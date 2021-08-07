"""Jobs Serializer"""

from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Jobs, JobsHistory
from notifications.serializers import NotificationsSerializer


class JobsSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    notifications = NotificationsSerializer(many=True, required=False)

    class Meta:
        model = Jobs
        fields = ['uuid', 'url', 'title', 'state', 'headers',
                  'notifications', 'verify_ssl', 'interval', 'success_status', 'check_redirect']
        read_only_fields = ['uuid']


class JobsHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = JobsHistory
        fields = ['timestamp', 'uuid', 'status_code',
                  'success', 'response_time', 'error']
        read_only_fields = fields
