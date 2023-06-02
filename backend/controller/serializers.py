"""Controller Serializer"""

from rest_framework import serializers


class JobUpdateMisfireGraceTimeSerializer(serializers.Serializer):
    grace_time = serializers.IntegerField(min_value=1, max_value=300)
