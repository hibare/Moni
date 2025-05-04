"""Accounts URLs"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from accounts.views import (
    APIToken,
    JWTTokenObtainPairView,
    AccountView,
    ChangePasswordView,
)

urlpatterns = [
    path(
        "",
        AccountView.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="account",
    ),
    path("password/", ChangePasswordView.as_view({"put": "update"}), name="passsword"),
    path("token/", APIToken.as_view(), name="api_token"),
    path("jwt/", JWTTokenObtainPairView.as_view(), name="jwt_obtain_pair"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
]
