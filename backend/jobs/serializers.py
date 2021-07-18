"""Jobs Serializer"""

from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Jobs, JobsHistory
from notification.serializers import NotificationSerializer


class JobsSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    notification_urls = NotificationSerializer(many=True, required=False)

    class Meta:
        model = Jobs
        fields = ['uuid', 'url', 'title', 'state', 'headers',
                  'notification_urls', 'verify_ssl', 'interval', 'success_status', 'check_redirect']
        read_only_fields = ['uuid']


class JobsHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = JobsHistory
        fields = ['timestamp', 'uuid', 'status_code',
                  'success', 'response_time']
        read_only_fields = fields
