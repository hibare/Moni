"""Controller Views"""

import logging

from controller.jobs import JobsController
from controller.serializers import JobUpdateMisfireGraceTimeSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class JobsControllerViewSet(viewsets.ViewSet):

    permission_classes = (permissions.IsAdminUser,)

    def update_misfire_grace_time(self, request, **kwargs):
        serializer = JobUpdateMisfireGraceTimeSerializer(data=request.data)

        if serializer.is_valid():

            uuid = kwargs.get("uuid", None)

            logger.info("UUID %s", uuid)
            if uuid is not None:
                JobsController.update_job_misfire_grace_time(uuid, serializer.data["grace_time"])
            else:
                JobsController.update_jobs_misfire_grace_time(serializer.data["grace_time"])

            return Response({"detail": "Job misfire grace time updated"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
