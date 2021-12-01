"""Accounts Views"""

import logging
from django.contrib.auth.models import User
from rest_framework import generics, serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import JWTTokenObtainPairSerializer, AccountSerializer, ChangePasswordSerializer

logger = logging.getLogger(__name__)


class APIToken(ObtainAuthToken):
    """API Token request handler"""

    def get_permissions(self):
        """
        Override get_permissions

        Check authentication for GET, PUT, DELETE
        """

        is_authenticated_methods = ['GET', 'PUT', 'DELETE']

        if self.request.method in is_authenticated_methods:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get(self, request, *args, **kwargs):
        """Retrieve API token"""

        user = request.user

        try:
            token = Token.objects.get(user=user)
            return Response({'token': token.key})
        except Token.DoesNotExist:
            raise NotFound

    def put(self, request, *args, **kwargs):
        """Regenerate API token"""

        user = request.user

        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass
        except Exception:
            logger.exception("Token update failed")
            return Response({'Details': 'Operation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    def delete(self, request, *args, **kwargs):
        """Delete API token"""

        user = request.user

        try:
            token = Token.objects.get(user=user)
            token.delete()
            return Response({'Details': 'Token deleted'})
        except Token.DoesNotExist:
            raise NotFound
        except Exception:
            logger.exception("Token deletion failed")
            return Response({'Details': 'Token deletion failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JWTTokenObtainPairView(TokenObtainPairView):
    serializer_class = JWTTokenObtainPairSerializer


class AccountView(viewsets.ViewSet):
    """User Account viewset"""

    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer
    queryset = User.objects.all()

    def retrieve(self, request, pk=None):
        user = self.queryset.get(username=request.user.username)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        user = request.user
        serializer = self.serializer_class(user, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(viewsets.ViewSet):
    """Password reset viewset"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, pk=None):
        user = request.user
        serializer = self.serializer_class(
            user, request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
