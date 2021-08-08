"""Notifications Views"""

import logging
from collections import Counter
from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from notifications.serializers import NotificationsSerializer, NotificationsHistorySerializer
from notifications.models import Notifications, NotificationsHistory
from notifications.services.notify import Notify

logger = logging.getLogger(__name__)


class NotificationsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Notifications views"""

    lookup_field = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationsSerializer
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

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def delivery(self, request, **kwargs):
        """Return notification delivery percentage"""

        try:
            uuid = self.kwargs['uuid']

            status_list = NotificationsHistory.objects.filter(
                uuid=uuid).values_list('status', flat=True)

            status_counter = Counter(status_list)

            delivery = round(status_counter[True] /
                             len(status_list) * 100.0, 2)

            return Response({"delivery": delivery}, status=status.HTTP_200_OK)

        except Notifications.DoesNotExist:
            raise NotFound

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def test(self, request, **kwargs):
        """Test notification endpoint"""

        n_status = n_status_code = n_error = None

        try:
            uuid = self.kwargs['uuid']

            queryset = Notifications.objects.get(uuid=uuid)

            n_status, n_status_code, n_error = Notify.test(queryset)

            if n_status:
                return Response({
                    "status": n_status,
                    "status_code": n_status_code,
                    "error": n_error
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": n_status,
                    "status_code": n_status_code,
                    "error": n_error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
