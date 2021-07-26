"""Accounts URLs"""

from django.urls import path
from accounts.views import APIToken

urlpatterns = [
    path('token/', APIToken.as_view(), name='token')
]
