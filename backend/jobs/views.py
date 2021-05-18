"""Jobs Views"""

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from jobs.models import Jobs
from jobs.serializers import JobsSerializer


class JobsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Jobs ViewSet"""

    lookup_field = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = JobsSerializer
    queryset = Jobs.objects.all()
