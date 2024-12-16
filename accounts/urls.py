from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("upload", AccountsUploadView.as_view(), name="accounts_upload"),
    path("list", AccountListView.as_view(), name="accounts_list"),
]
