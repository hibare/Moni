"""Jobs Serializer"""

from rest_framework import serializers
from .models import Notifications, NotificationsHistory


class NotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = '__all__'
        read_only_fields = ['uuid']


class NotificationsHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationsHistory
        fields = '__all__'
        read_only_fields = fields
