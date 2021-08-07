"""Accounts Views"""

import logging
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status, permissions


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
