"""Jobs Serializer"""

from rest_framework.fields import ReadOnlyField
from .models import Jobs
from rest_framework import serializers


class JobsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Jobs
        fields = ['url', 'title', 'state',
                  'notify_url', 'verify_ssl', 'interval', 'success_status', 'check_redirect']
        read_only_fields = ['uuid']
