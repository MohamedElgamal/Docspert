from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from io import StringIO
from accounts.models import Account
from accounts.forms import AccountsUploadForm

class AccountsHomeViewTest(TestCase):
    """Responsible of testing AccountsHomeView located in accounts.views"""
    def setUp(self):
        self.client = Client()
        self.url = reverse("accounts_home") 

    def test_get_accounts_home_view(self):
        """test status code is 200 and returned template (accounts-home.html)"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts-home.html")

class AccountsListViewTest(TestCase):
    """Responsible of testing AccountsListView located in accounts.views"""
    def setUp(self):
        self.client = Client()
        self.url = reverse("accounts_list")  
        self.account1 = Account.objects.create(name="Test Account 1", balance=120.05)
        self.account2 = Account.objects.create(name="Test Account 2", balance=90501)

    def test_get_accounts_list_view(self):
        """Test status code, template and response return all records in db"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts-list.html")
        self.assertIn(self.account1, response.context["accounts"]) # Check if account1 record are exists in response
        self.assertIn(self.account2, response.context["accounts"])

    def test_get_accounts_list_view_with_search_query(self):
        """Test that search query functionality work correctly and only data related to search query are returned"""
        response = self.client.get(self.url, {"search_query": "Account 1"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts-list.html")
        self.assertIn(self.account1, response.context["accounts"])# Check if account1 are returned or not, it should be returned 
        self.assertNotIn(self.account2, response.context["accounts"])# account2 should not exists in returned response 

    def test_get_accounts_list_view_with_no_results(self):
        """Test that it will return 0 records, if search query not corresponding to any record"""
        response = self.client.get(self.url, {"search_query": "DevMohamedElGamalNOTEXISTS"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts-list.html")
        self.assertEqual(len(response.context["accounts"]), 0)

class AccountSearchViewTest(TestCase):
    """Similar to AccountsListViewTest but with json format instead"""
    def setUp(self):
        self.client = Client()
        self.url = reverse("account_search")
        self.account1 = Account.objects.create(name="Search Account 1", balance=150)
        self.account2 = Account.objects.create(name="Other Account", balance=300)

    def test_get_account_search_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)  # All accounts are returned

    def test_get_account_search_view_with_query(self):
        response = self.client.get(self.url, {"search_query": "Search"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)  # Only one account matches the search
        self.assertEqual(data[0]["name"], "Search Account 1")

    def test_get_account_search_view_with_no_results(self):
        response = self.client.get(self.url, {"search_query": "Nonexistent"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

class AccountDetailsViewTest(TestCase):
    """Responsible of Testing AccountDetailsView"""
    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(name="Dev. Mohamed ElGamal", balance=25000)
        self.url = reverse("account_details", args=[self.account.id])

    def test_get_account_details_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account-details.html")
        self.assertEqual(response.context["account"], self.account)


class AccountTransferFundsViewTest(TestCase):
    """Responsible of Testing AccountTransferFundsView"""
    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(name="Transfer Account", balance=700)
        self.url = reverse("account_transfer_fund", args=[self.account.id])

    def test_get_account_transfer_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account-transfer.html")
        self.assertEqual(response.context["account"], self.account)

class TransferFundsViewTest(TestCase):
    """Responsible of Testing TransferFundsView that hold all logic related to transfer balance from account 
    to another account."""
    def setUp(self):
        self.client = Client()
        self.account_from = Account.objects.create(name="Account From", balance=500)
        self.account_to = Account.objects.create(name="Account To", balance=300)
        self.url = reverse("transfer_balance")

    def test_transfer_funds_success(self):
        """Test case that transfer from has sufficient balance and balance to be transferred is less or equal to allowed value"""
        response = self.client.get(
            self.url,
            {
                "transfer_from": self.account_from.id,
                "transfer_to": self.account_to.id,
                "transfer_balance": 100,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Transfer successful") # Check if the response has desired message
        self.account_from.refresh_from_db()
        self.account_to.refresh_from_db()
        self.assertEqual(self.account_from.balance, 400)
        self.assertEqual(self.account_to.balance, 400)

    def test_transfer_funds_missing_parameters(self):
        """Test case, check if code handle if there is missing parameters or not"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Missing required parameters")

    def test_transfer_funds_insufficient_balance(self):
        """Test case, if user try to transfer balance greater than allowed balance or equal or less than zero"""
        response = self.client.get(
            self.url,
            {
                "transfer_from": self.account_from.id,
                "transfer_to": self.account_to.id,
                "transfer_balance": 600,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Insufficient balance")

    def test_transfer_funds_to_self(self):
        """Test the case if user try to transfer balance to himself to break the equation"""
        response = self.client.get(
            self.url,
            {
                "transfer_from": self.account_from.id,
                "transfer_to": self.account_from.id,
                "transfer_balance": 100,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Cannot transfer to himself")

    def test_transfer_funds_invalid_account(self):
        """Test case if someone try modify in the client side and set the ids to non-existing users"""
        response = self.client.get(
            self.url,
            {
                "transfer_from": "00000000-0000-0000-0000-000000000000",  # Nonexistent UUID
                "transfer_to": self.account_to.id,
                "transfer_balance": 100,
            },
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Account not found")


class AccountsUploadFormTestCase(TestCase):

    def setUp(self):
        # Set up necessary variables for tests
        self.valid_csv_content = (
            "ID,Name,Balance\n"
            "cc26b56c-36f6-41f1-b689-d1d5065b95af,Joy Dean,4497.22\n"
            "be6acfdc-cae1-4611-b3b2-dfb5167ba5fe,Bryan Rice,2632.76\n"
            "43caa0b8-76a4-4e61-b7c3-f2f5ee4b4f77,Ms. Jamie Lopez,1827.85\n"
            "69c93967-e20f-4735-9b8d-1b7dd56340ab,Lauren David,9778.70\n"
            "60c233f0-1bfa-4f00-b1b3-5b6443c2670e,Gregory Elliott,1926.39"
        )
        self.invalid_csv_content_missing_header = (
            "ID,Name\n"
            "cc26b56c-36f6-41f1-b689-d1d5065b95af,Joy Dean"
        )

    def test_valid_csv_file(self):
        """Test valid CSV file with correct headers"""
        form_data = {
            'file': self.create_file(self.valid_csv_content, 'text/csv')
        }
        form = AccountsUploadForm(data=form_data)
        self.assertTrue(form.is_valid())
        data = form.cleaned_data['file']
        self.assertEqual(len(data), 5)  # Check the len of dict is equal to 5

    def test_invalid_csv_file_missing_header(self):
        """Test CSV file with missing required header"""
        form_data = {
            'file': self.create_file(self.invalid_csv_content_missing_header, 'text/csv')
        }
        form = AccountsUploadForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors) 

    def create_file(self, content, content_type):
        """Helper method to create an in-memory file for testing"""
        file = StringIO(content)
        file.name = 'test_file.csv' if content_type == 'text/csv' else 'test_file.txt'
        file.content_type = content_type
        return file