from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic import View, ListView, DetailView
from django.urls import reverse_lazy, reverse
from .forms import AccountsUploadForm
from .models import Account
import csv

# Create your views here.


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


class AccountDetailsView(DetailView):
    """Handle account details"""

    model = Account
    template_name = "account-details.html"
    context_object_name = "account"


class AccountTransferFundsView(DetailView):
    """Handle account transfer funds"""

    model = Account
    template_name = "account-transfer.html"

    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk)

        search_value = request.GET.get("search_query", "")
        transfer_to_id = request.GET.get("transfer-to-id", None)
        print("Test: ")
        print(transfer_to_id)
        search_accounts = []
        if search_value:
            search_accounts = Account.objects.filter(name__icontains=search_value)
            print(search_accounts)

        # Return the context with the account and search results
        context = {
            "search_value": search_value,
            "account": account,
            "search_accounts": search_accounts,
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        # Handle the transfer logic here (e.g., get form data, validate, transfer funds)
        # You can process the form submission and perform the necessary actions
        # For example:
        account = get_object_or_404(Account, pk=pk)
        # process transfer, like updating account balances

        # Redirect after the transfer is successful (you can modify this logic as needed)
        return HttpResponseRedirect(reverse("account_transfer_fund", kwargs={"pk": pk}))
