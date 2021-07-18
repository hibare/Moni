"""Jobs Serializer"""

from rest_framework import serializers
from .models import Notifications


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = ['uuid', 'url', 'type', 'description']
        read_only_fields = ['uuid']
