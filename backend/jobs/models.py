"""Jobs Models"""

from datetime import timedelta
from typing import List
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField
from model_utils import FieldTracker
from moni.utils.favicon import Favicon
from moni.utils.funcs import get_str_uuid
from notifiers.models import Notifiers


def default_success_status() -> List[int]:
    """Default Success status code"""

    return [200]


class Jobs(models.Model):
    """Health Check jobs"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uuid = models.CharField(max_length=40, default=get_str_uuid, primary_key=True)
    url = models.URLField(unique=True)
    title = models.CharField(max_length=15)
    # Job state aka, enabled or disabled
    state = models.BooleanField(default=True)
    headers = models.JSONField(default=dict)
    notifiers = models.ManyToManyField(
        Notifiers, related_name="jobs_notifiers", db_column="uuid", blank=True
    )
    verify_ssl = models.BooleanField(default=True)
    interval = models.PositiveIntegerField(default=15)
    success_status = ArrayField(
        models.PositiveIntegerField(), default=default_success_status
    )
    check_redirect = models.BooleanField(default=True)
    healthy = models.BooleanField(default=True)
    favicon_url = models.URLField(null=True, blank=True)
    failure_threshold = models.PositiveIntegerField(default=1)

    tracker = FieldTracker()

    class Meta:
        indexes = [
            models.Index(fields=["uuid"]),
        ]
        verbose_name = "Jobs"
        verbose_name_plural = "Jobs"

    def __str__(self) -> str:
        return self.uuid

    def update_favicon_url(self):
        self.favicon_url = Favicon.get_favicon_url(self.url)
        self.save()


class JobsHistoryManager(models.Manager):
    """Job history manager"""

    def delete_old_history(self, max_age: int) -> None:
        """Delete job history from database"""

        self.filter(timestamp__lte=timezone.now() - timedelta(days=max_age)).delete()


class JobsHistory(models.Model):
    """Health check jobs execution history"""

    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.ForeignKey(
        Jobs, related_name="jobs_history_uuid", on_delete=models.CASCADE
    )
    status_code = models.IntegerField(null=True, blank=True)
    success = models.BooleanField()
    response_time = models.FloatField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)

    objects = JobsHistoryManager()

    class Meta:
        indexes = [
            models.Index(fields=["uuid"]),
            models.Index(fields=["-timestamp", "uuid"]),
        ]
        verbose_name = "Jobs History"
        verbose_name_plural = "Jobs History"
