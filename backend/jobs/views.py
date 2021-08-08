"""Jobs Views"""

import logging
from collections import Counter
from statistics import mean
from rest_framework import viewsets, mixins, generics, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from jobs.models import Jobs, JobsHistory
from jobs.serializers import JobsSerializer, JobsHistorySerializer

logger = logging.getLogger(__name__)


class JobsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Jobs ViewSet"""

    lookup_field = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = JobsSerializer
    queryset = Jobs.objects.all()

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def history(self, request, **kwargs):
        """Return Job execution history"""

        uuid = self.kwargs['uuid']

        queryset = JobsHistory.objects.filter(uuid=uuid)

        if queryset.exists():
            serializer = JobsHistorySerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise NotFound()

    @history.mapping.delete
    def history_delete(self, request, **kwargs):
        """Delete Job execution history"""

        uuid = self.kwargs['uuid']

        queryset = JobsHistory.objects.filter(uuid=uuid)

        if queryset.exists():
            queryset.delete()
            return Response({"detail": "Job history deleted"}, status=status.HTTP_200_OK)
        else:
            raise NotFound()

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def pause(self, request, **kwargs):
        """Pause job"""

        try:
            uuid = self.kwargs['uuid']

            job = self.queryset.get(uuid=uuid)

            if job.state:
                job.state = False
                job.save()

                return Response({"detail": "Job paused"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Job already in pause state"}, status=status.HTTP_409_CONFLICT)
        except Jobs.DoesNotExist:
            raise NotFound

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def resume(self, request, **kwargs):
        """Resume job"""

        try:
            uuid = self.kwargs['uuid']

            job = self.queryset.get(uuid=uuid)

            if not job.state:
                job.state = True
                job.save()

                return Response({"detail": "Job resumed"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Job already in active state"}, status=status.HTTP_409_CONFLICT)
        except Jobs.DoesNotExist:
            raise NotFound

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def uptime(self, request, **kwargs):
        """Return job uptime (percentage)"""

        try:
            uuid = self.kwargs['uuid']

            success_list = JobsHistory.objects.filter(
                uuid=uuid).values_list('success', flat=True)

            if success_list.exists():
                success_counter = Counter(success_list)

                uptime = round(success_counter[True] /
                               len(success_list) * 100.0, 2)
                uptime = str(uptime) + '%'
            else:
                uptime = "-"

            return Response({"uptime": uptime}, status=status.HTTP_200_OK)

        except Jobs.DoesNotExist:
            raise NotFound

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def response(self, request, **kwargs):
        """Job response time (avg. seconds)"""

        try:
            uuid = self.kwargs['uuid']
            response_list = JobsHistory.objects.filter(uuid=uuid).exclude(
                response_time__isnull=True).values_list('response_time', flat=True)

            if response_list.exists():
                response = round(mean(response_list), 2)
                response = str(response) + 'sec'
            else:
                response = "-"

            return Response({"response": response}, status=status.HTTP_200_OK)
        except Jobs.DoesNotExist:
            raise NotFound


class JobsHistoryViewSet(generics.ListAPIView, viewsets.GenericViewSet):
    """
    Jobs History ViewSet

    /api/v1/jobs/history/
    """

    lookup_field = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = JobsHistorySerializer
    queryset = JobsHistory.objects.all()
