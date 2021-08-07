"""Jobs Serializer"""

from rest_framework import serializers
from .models import Notifications, NotificationsHistory


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = ['uuid', 'url', 'type', 'description']
        read_only_fields = ['uuid']


class NotificationsHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationsHistory
        fields = ['uuid', 'status', 'status_code', 'error']
        read_only_fields = fields
