"""Jobs Views"""

from rest_framework import viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from jobs.models import Jobs, JobsHistory
from jobs.serializers import JobsSerializer, JobsHistorySerializer


class JobsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Jobs ViewSet"""

    lookup_field = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = JobsSerializer
    queryset = Jobs.objects.all()


class JobsHistoryViewSet(generics.ListAPIView, viewsets.GenericViewSet, generics.RetrieveAPIView):
    """
    Jobs History ViewSet

    /api/v1/jobs/history/
    /api/v1/jobs/history/uuid=97e488cf-d847-4668-a6d9-1ee7dc0f00b2/
    """

    lookup_field = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = JobsHistorySerializer
    queryset = JobsHistory.objects.all()

    def retrieve(self, request, *args, **kwargs):
        uuid = self.kwargs.get('uuid')

        if uuid is None:
            return self.queryset()
        else:
            queryset = self.queryset.filter(uuid=uuid)

            if queryset.exists():
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                raise NotFound()
