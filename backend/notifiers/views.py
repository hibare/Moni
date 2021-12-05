"""Notifiers Views"""

import logging
from collections import Counter
from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from notifiers.serializers import NotifiersSerializer, NotifiersHistorySerializer, NotifierTestSerializer
from notifiers.models import Notifiers, NotifiersHistory
from notifiers.services.notify import Notify
from jobs.models import Jobs
from jobs.serializers import JobsSerializer

logger = logging.getLogger(__name__)


class NotifiersViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Notifiers views"""

    lookup_field = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = NotifiersSerializer
    queryset = Notifiers.objects.all()

    def list(self, request, *args, **kwargs):
        """Override default list method.
        Check for type & filter based on it.
        Default apply no filter
        """
        queryset = self.get_queryset()

        if request.query_params.get('type'):
            result = queryset.filter(type=request.query_params.get('type'))
        else:
            result = queryset
        serializer = self.serializer_class(result, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def history(self, request, **kwargs):
        """Return a notifier execution history"""

        uuid = self.kwargs['uuid']

        queryset = NotifiersHistory.objects.filter(
            uuid=uuid).order_by('-timestamp')

        serializer = NotifiersHistorySerializer(queryset, many=True)
        return Response(serializer.data)

    @history.mapping.delete
    def history_delete(self, request, **kwargs):
        """Delete a notifier execution history"""

        uuid = self.kwargs['uuid']

        queryset = NotifiersHistory.objects.filter(uuid=uuid)

        if queryset.exists():
            queryset.delete()
            return Response({"detail": "Notifier history deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            raise NotFound()

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def delivery(self, request, **kwargs):
        """Return notifier delivery percentage"""

        try:
            uuid = self.kwargs['uuid']

            status_list = NotifiersHistory.objects.filter(
                uuid=uuid).values_list('status', flat=True)

            if status_list.exists():

                status_counter = Counter(status_list)

                delivery = round(status_counter[True] /
                                 len(status_list) * 100.0, 2)

                delivery = str(delivery) + '%'
            else:
                delivery = "-"

            return Response({"delivery": delivery}, status=status.HTTP_200_OK)

        except Notifiers.DoesNotExist:
            raise NotFound

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def jobs(self, request, **kwargs):
        """Return all jobs using this notifier"""

        try:
            uuid = self.kwargs['uuid']

            _ = Notifiers.objects.get(
                uuid=uuid)

            query_set = Jobs.objects.filter(notifiers=uuid)

            serializer = JobsSerializer(query_set, many=True)
            return Response(serializer.data)

        except Notifiers.DoesNotExist:
            return Response({"detail": "Invalid notifier"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True, url_path="test", permission_classes=[IsAuthenticated])
    def saved_test(self, request, **kwargs):
        """
        Test notifier endpoint.
        To be used on notifiers which are already created & saved.
        """

        n_status = n_status_code = n_error = None

        try:
            uuid = self.kwargs['uuid']

            queryset = Notifiers.objects.get(uuid=uuid)

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
                }, status=n_status_code)
        except Notifiers.DoesNotExist:
            raise NotFound

    @action(methods=['post'], detail=False, url_path="test", permission_classes=[IsAuthenticated])
    def unsaved_test(self, request, **kwargs):
        """
        Test notifier endpoint
        To be used on notifiers which are not yet created.
        """

        n_status = n_status_code = n_error = None

        serializer = NotifierTestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        notifier = Notifiers(
            url=request.data['url'],
            type=request.data['type']
        )

        n_status, n_status_code, n_error = Notify.test(notifier)

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
            }, status=n_status_code)


class NotifiersHistoryViewSet(generics.ListAPIView, viewsets.GenericViewSet):
    """
    Notificaitons History ViewSet

    /api/v1/notifiers/history/
    """

    lookup_field = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = NotifiersHistorySerializer
    queryset = NotifiersHistory.objects.all()
