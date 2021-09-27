"""Jobs Serializer"""

from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Jobs, JobsHistory
from notifiers.serializers import NotifiersSerializer


class JobsSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    notifiers = NotifiersSerializer(many=True, required=False)

    class Meta:
        model = Jobs
        fields = '__all__'
        read_only_fields = ['uuid']


class JobsHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = JobsHistory
        fields = '__all__'
        read_only_fields = ['timestamp', 'uuid',
                            'status_code', 'success', 'response_time', 'error']
