"""Notifier Serializer"""

from rest_framework import serializers

from .models import Notifiers, NotifiersHistory


class NotifiersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifiers
        fields = "__all__"
        read_only_fields = ["uuid"]


class NotifiersHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NotifiersHistory
        fields = "__all__"
        read_only_fields = ["timestamp", "uuid", "status_code", "error"]


class NotifierTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifiers
        fields = ["url", "type"]
        extra_kwargs = {
            "url": {"validators": []},
        }
