from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("upload", AccountsUploadView.as_view(), name="accounts_upload"),
    path("list", AccountsListView.as_view(), name="accounts_list"),
    path("search", AccountSearchView.as_view(), name="account_search"),
    path("details/<uuid:pk>", AccountDetailsView.as_view(), name="account_details"),
    path("transfer/<uuid:pk>", AccountTransferFundsView.as_view(), name="account_transfer_fund"),
    path("tranfer-balance", TransferFundsView.as_view(), name="transfer_balance")
]
