"""Jobs Models"""

from django.db import models
from django.contrib.postgres.fields import ArrayField
from model_utils import FieldTracker
from moni.utils.funcs import get_str_uuid
from jobs.validators import apprise_url_validator


def default_success_status():
    """Default Success status code"""

    return [200]


class Jobs(models.Model):
    """Health Check jobs"""

    uuid = models.CharField(
        max_length=40, default=get_str_uuid, primary_key=True)
    url = models.URLField(unique=True)
    title = models.CharField(max_length=50)
    state = models.BooleanField(default=True)
    notify_url = models.URLField(null=True, validators=[apprise_url_validator])
    verify_ssl = models.BooleanField(default=True)
    interval = models.IntegerField(default=15)
    success_status = ArrayField(
        models.IntegerField(), default=default_success_status)
    check_redirect = models.BooleanField(default=True)

    tracker = FieldTracker()

    class Meta:
        verbose_name = "Jobs"
        verbose_name_plural = "Jobs"


class JobsHistory(models.Model):
    """Health check jobs execution history"""

    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.ForeignKey(
        Jobs, related_name="jobs_history_uuid", on_delete=models.CASCADE)
    status_code = models.IntegerField(null=True)
    success = models.BooleanField()

    class Meta:
        verbose_name = "Jobs History"
        verbose_name_plural = "Jobs History"
