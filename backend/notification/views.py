"""Notification Views"""

import logging
from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from notification.serializers import NotificationSerializer, NotificationsHistorySerializer
from notification.models import Notifications, NotificationsHistory
from notification.services.slack.slack import Slack
from notification.services.discord.discord import Discord
from notification.services.webhook.webhook import Webhook
from notification.services.gotify.gotify import Gotify

logger = logging.getLogger(__name__)


class NotificationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Notification views"""

    lookup_field = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer
    queryset = Notifications.objects.all()

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def history(self, request, **kwargs):
        """Return a notification execution history"""

        uuid = self.kwargs['uuid']

        queryset = NotificationsHistory.objects.filter(uuid=uuid)

        if queryset.exists():
            serializer = NotificationsHistorySerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise NotFound()

    @history.mapping.delete
    def history_delete(self, request, **kwargs):
        """Delete a notification execution history"""

        uuid = self.kwargs['uuid']

        queryset = NotificationsHistory.objects.filter(uuid=uuid)

        if queryset.exists():
            queryset.delete()
            return Response({"detail": "Notification history deleted"}, status=status.HTTP_200_OK)
        else:
            raise NotFound()

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def test(self, request, **kwargs):
        """Test notification endpoint"""

        state = False

        try:
            uuid = self.kwargs['uuid']

            queryset = Notifications.objects.get(uuid=uuid)

            if queryset.type == 'slack':
                notify = Slack()
                state = notify.send(queryset.url)

            elif queryset.type == 'discord':
                notify = Discord()
                state = notify.send(queryset.url)

            elif queryset.type == 'webhook':
                notify = Webhook()
                state = notify.send(queryset.url)

            elif queryset.type == 'gotify':
                notify = Gotify()
                state = notify.send(queryset.url)

            if state:
                return Response({"detail": "Success"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Notifications.DoesNotExist:
            raise NotFound


class NotificationsHistoryViewSet(generics.ListAPIView, viewsets.GenericViewSet):
    """
    Notificaitons History ViewSet

    /api/v1/notifications/history/
    """

    lookup_field = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationsHistorySerializer
    queryset = NotificationsHistory.objects.all()
