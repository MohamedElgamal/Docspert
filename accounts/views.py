from django.shortcuts import render
from django.views.generic import View, ListView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import AccountsUploadForm
from .models import Account
import csv

# Create your views here.


class AccountsUploadView(View):
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
        try:
            accounts = [Account(**record) for record in data]
            Account.objects.bulk_create(
                accounts, ignore_conflicts=True
            )  # ignore confict to not raise error if user upload the file more than one time only will insert the new records each time.
        except Exception as e:
            raise


class AccountListView(ListView):
    model = Account
    template_name = "accounts-list.html"
