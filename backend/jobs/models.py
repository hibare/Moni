"""Jobs Models"""

from django.db import models
from model_utils import FieldTracker
from moni.utils.funcs import get_str_uuid


class Jobs(models.Model):
    """Health Check jobs"""

    uuid = models.CharField(
        max_length=40, default=get_str_uuid(), primary_key=True)
    url = models.URLField(unique=True)
    title = models.CharField(max_length=50)
    state = models.BooleanField(default=True)
    notify_url = models.URLField(null=True)
    verify_ssl = models.BooleanField(default=True)
    interval = models.IntegerField(default=15)
    success_status = models.IntegerField(default=200)
    check_redirect = models.BooleanField(default=True)

    tracker = FieldTracker()

    class Meta:
        verbose_name = "Jobs"
        verbose_name_plural = "Jobs"
