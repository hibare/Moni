"""Jobs Serializer"""

from notifiers.models import Notifiers
from rest_framework import serializers

from .models import Jobs, JobsHistory


class JobsSerializer(serializers.ModelSerializer):
    notifiers = serializers.PrimaryKeyRelatedField(many=True, queryset=Notifiers.objects.all())

    def validate_failure_threshold(self, value):
        """
        failure_threshold should be always greater than 0.
        """

        if value <= 0:
            raise serializers.ValidationError(detail="Value must be greater than 0", code="failure_threshold")
        return value

    class Meta:
        model = Jobs
        fields = "__all__"
        read_only_fields = ["uuid", "healthy"]


class JobsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobsHistory
        fields = "__all__"
        read_only_fields = [
            "timestamp",
            "uuid",
            "status_code",
            "success",
            "response_time",
            "error",
        ]
