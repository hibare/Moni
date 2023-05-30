"""Jobs Views"""

import logging
from collections import Counter
from statistics import mean
from rest_framework import viewsets, mixins, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from jobs.models import Jobs, JobsHistory
from jobs.serializers import JobsSerializer, JobsHistorySerializer
from moni.utils.favicon import Favicon
from notifiers.models import Notifiers
from notifiers.serializers import NotifiersSerializer

logger = logging.getLogger(__name__)


class JobsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Jobs ViewSet"""

    lookup_field = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = JobsSerializer
    queryset = Jobs.objects.all()

    @action(methods=['get'], detail=False, permission_classes=[AllowAny])
    def status(self, request, **kwargs):
        """
        Return a flag indicating overall status of all jobs
        Status=True indicates all jobs healthy
        Status=False indicates one of the job is un-healthy
        Jobs=int indicates no. of jobs having corresponding status.
        """

        if self.queryset.exists():
            health = [job.healthy for job in self.queryset.filter(state=True)]

            if health.count(False):
                return Response({"status": False, "jobs": health.count(False)}, status=status.HTTP_200_OK)
            else:
                return Response({"status": True, "jobs": health.count(True)}, status=status.HTTP_200_OK)
        else:
            return Response({"status": None, "jobs": None}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def history(self, request, **kwargs):
        """Return Job execution history"""

        uuid = self.kwargs['uuid']

        queryset = JobsHistory.objects.filter(uuid=uuid).order_by('-timestamp')

        serializer = JobsHistorySerializer(queryset, many=True)
        return Response(serializer.data)

    @history.mapping.delete
    def history_delete(self, request, **kwargs):
        """Delete Job execution history"""

        uuid = self.kwargs['uuid']

        queryset = JobsHistory.objects.filter(uuid=uuid)

        if queryset.exists():
            queryset.delete()
            return Response({"detail": "Job history deleted"}, status=status.HTTP_204_NO_CONTENT)
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
                response = str(response) + ' sec'
            else:
                response = "-"

            return Response({"response": response}, status=status.HTTP_200_OK)
        except Jobs.DoesNotExist:
            raise NotFound

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def favicon(self, request, **kwargs):
        """
        Update favicon URL with the latest one.
        Send status 200 irrespective of actual status.
        """

        try:
            uuid = self.kwargs['uuid']

            job = self.queryset.get(uuid=uuid)

            favicon_url = Favicon.get_favicon_url(job.url)

            job.favicon_url = favicon_url
            job.save()

            return Response(self.serializer_class(job).data)
        except Jobs.DoesNotExist:
            raise NotFound

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def notifiers(self, request, **kwargs):
        """Return job notifiers"""

        try:
            uuid = self.kwargs['uuid']
            job = self.queryset.get(uuid=uuid)
            notifiers_uuids = job.notifiers.all().values_list('uuid', flat=True)
            queryset = Notifiers.objects.filter(uuid__in=notifiers_uuids)
            serializer = NotifiersSerializer(queryset, many=True)
            return Response(serializer.data)
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
