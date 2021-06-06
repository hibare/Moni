"""Jobs Serializer"""

from rest_framework import serializers
from .models import Jobs, default_success_status


class JobsSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.CharField(
        max_length=40,
        read_only=True
    )
    url = serializers.URLField(
        help_text="URL to run health check against",
        required=True
    )
    title = serializers.CharField(
        max_length=40,
        help_text="Title for easy identification of this job",
        required=True
    )
    state = serializers.BooleanField(
        default=True,
        initial=True,
        help_text="State of the job"
    )
    notify_url = serializers.URLField(
        default=None,
        allow_null=True,
        help_text="Notification URL used when healthcheck fails"
    )
    verify_ssl = serializers.BooleanField(
        default=True,
        initial=True,
        help_text="Verify SSL certificate"
    )
    interval = serializers.IntegerField(
        default=15,
        initial=15,
        help_text="Job interval in minutes"
    )
    success_status = serializers.ListField(
        child=serializers.IntegerField(),
        default=default_success_status(),
        help_text="HTTP status to check health check response status for success"
    )
    check_redirect = serializers.BooleanField(
        default=True,
        initial=True,
        help_text="Check for redirects"
    )

    class Meta:
        model = Jobs
        fields = ['uuid', 'url', 'title', 'state',
                  'notify_url', 'verify_ssl', 'interval', 'success_status', 'check_redirect']
