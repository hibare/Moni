"""Notifiers models"""

from datetime import timedelta
from django.utils import timezone
from django.db import models
from moni.utils.funcs import get_str_uuid


class Notifiers(models.Model):
    """Notifiers"""

    NOTIFIER_TYPES = [
        ("slack", "Slack"),
        ("discord", "Discord"),
        ("webhook", "Webhook"),
        ("gotify", "Gotify"),
        ("telegram", "Telegram")
    ]

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uuid = models.CharField(
        max_length=40, default=get_str_uuid, primary_key=True)
    url = models.URLField(unique=True)
    type = models.CharField(max_length=10, choices=NOTIFIER_TYPES)
    title = models.CharField(max_length=15)
    description = models.TextField(default="", blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['uuid']),
        ]
        verbose_name = "Notifiers"
        verbose_name_plural = "Notifiers"

    def __str__(self) -> str:
        return self.uuid


class NotifiersHistoryManager(models.Manager):
    """Notifiers history manager"""

    def delete_old_history(self, max_age: int) -> None:
        """Delete notifiers history from database"""

        self.filter(timestamp__lte=timezone.now() -
                    timedelta(seconds=max_age)).delete()


class NotifiersHistory(models.Model):
    """Notifiers execution history"""

    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.ForeignKey(
        Notifiers, related_name="notifier_uuid", on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    status_code = models.IntegerField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)

    objects = NotifiersHistoryManager()

    class Meta:
        indexes = [
            models.Index(fields=['uuid']),
            models.Index(fields=['-timestamp', 'uuid'])
        ]
        verbose_name = "Notifiers History"
        verbose_name_plural = "Notifiers History"

    def __str__(self) -> str:
        return self.uuid.uuid
