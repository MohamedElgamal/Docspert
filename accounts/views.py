from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View, ListView, DetailView
from django.urls import reverse_lazy
from .forms import AccountsUploadForm
from .models import Account
from decimal import Decimal


# Create your views here.


class AccountsHomeView(View):
    """Responsible of returning home page of accounts"""

    template_name = "accounts-home.html"

    def get(self, request):
        return render(request, self.template_name)


class AccountsUploadView(View):
    """Handle upload the file that contain the accounts to server and save it into database"""

    template_name = "accounts-upload.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "form": AccountsUploadForm(),
            },
        )

    def post(self, request):
        """Receive uploaded file then validate the file according to result of validation, page will be rendered"""
        upload_form = AccountsUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            data = upload_form.cleaned_data["file"]
            try:
                self.save_accounts(data)
            except Exception as e:
                return render(request, "500.html", {"error_message": e})
        else:
            return render(
                request,
                self.template_name,
                {
                    "form": upload_form,
                },
            )
        success_url = reverse_lazy("accounts_list")
        return redirect(success_url)

    def save_accounts(self, data):
        """Save accounts into database"""
        try:
            accounts = [Account(**record) for record in data]
            Account.objects.bulk_create(
                accounts, ignore_conflicts=True
            )  # ignore confict to not raise error if user upload the file more than one time only will insert the new records each time.
        except Exception as e:
            raise


class AccountsListView(ListView):
    """Handle Listing of accounts & search for specific account using name"""

    model = Account
    template_name = "accounts-list.html"
    context_object_name = "accounts"

    def get_queryset(self):
        query_set = super().get_queryset()
        search_value = self.request.GET.get("search_query", "")
        if search_value:
            query_set = query_set.filter(
                name__icontains=search_value
            )  # Filter and return only all records that contain search_value as part of account name
        return query_set


class AccountSearchView(ListView):
    """Handle Listing of accounts & search for specific account using name, return json obj"""

    model = Account

    def get_queryset(self):
        query_set = super().get_queryset()
        search_value = self.request.GET.get("search_query", "")
        if search_value:
            query_set = query_set.filter(
                name__icontains=search_value
            )  # Filter and return only all records that contain search_value as part of account name
        return query_set

    def render_to_response(self, context):
        data = list(self.get_queryset().values())
        return JsonResponse(data, safe=False)


class AccountDetailsView(DetailView):
    """Handle account details"""

    model = Account
    template_name = "account-details.html"
    context_object_name = "account"


class AccountTransferFundsView(DetailView):
    """Display transfer account page"""

    model = Account
    template_name = "account-transfer.html"
    context_object_name = "account"


class TransferFundsView(View):
    """Handle and validate transferring balance between two accounts"""

    model = Account

    def get(self, request):
        transfer_from = request.GET.get("transfer_from")
        transfer_to = request.GET.get("transfer_to")
        transfer_balance = request.GET.get("transfer_balance")

        if not transfer_from or not transfer_to or not transfer_balance:
            return JsonResponse({"error": "Missing required parameters"}, status=400)

        try:
            transfer_from_account = Account.objects.get(id=transfer_from)
            transfer_to_account = Account.objects.get(id=transfer_to)
            transfer_balance = Decimal(transfer_balance)

            # Check if user try to tranfer to himself
            if transfer_from_account == transfer_to_account:
                return JsonResponse({"error": "Cannot transfer to himself"}, status=400)
            # Check if transfer_from account has enough balance
            if transfer_from_account.balance < transfer_balance:
                return JsonResponse({"error": "Insufficient balance"}, status=400)

            transfer_from_account.balance -= transfer_balance
            transfer_to_account.balance += transfer_balance
            transfer_from_account.save()
            transfer_to_account.save()

            return JsonResponse({"message": "Transfer successful"}, status=200)

        except Account.DoesNotExist:
            return JsonResponse({"error": "Account not found"}, status=404)
        except ValueError:
            return JsonResponse({"error": "Invalid transfer balance"}, status=400)
