"""Notification Views"""

import logging
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from notification.serializers import NotificationSerializer
from notification.models import Notifications

logger = logging.getLogger(__name__)


class NotificationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Notification views"""

    lookup_field = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer
    queryset = Notifications.objects.all()
