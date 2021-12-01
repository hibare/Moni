"""Jobs Serializer"""

from rest_framework import serializers
from .models import Jobs, JobsHistory
from notifiers.models import Notifiers


class JobsSerializer(serializers.ModelSerializer):
    notifiers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Notifiers.objects.all())

    class Meta:
        model = Jobs
        fields = '__all__'
        read_only_fields = ['uuid', 'healthy']


class JobsHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = JobsHistory
        fields = '__all__'
        read_only_fields = ['timestamp', 'uuid',
                            'status_code', 'success', 'response_time', 'error']
