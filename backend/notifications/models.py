"""Notifications models"""

from datetime import timedelta
from django.utils import timezone
from django.db import models
from moni.utils.funcs import get_str_uuid


class Notifications(models.Model):
    """Notifications"""

    NOTIFICATION_TYPES = [
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
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    description = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['uuid']),
        ]
        verbose_name = "Notifications"
        verbose_name_plural = "Notifications"


class NotificationsHistoryManager(models.Manager):
    """Notifications history manager"""

    def delete_old_history(self, max_age: int) -> None:
        """Delete notifications history from database"""

        self.filter(timestamp__lte=timezone.now() -
                    timedelta(seconds=max_age)).delete()


class NotificationsHistory(models.Model):
    """Notifications execution history"""

    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.ForeignKey(
        Notifications, related_name="notifications_uuid", on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    status_code = models.IntegerField(null=True)
    error = models.TextField(null=True)

    objects = NotificationsHistoryManager()

    class Meta:
        indexes = [
            models.Index(fields=['uuid']),
            models.Index(fields=['-timestamp', 'uuid'])
        ]
        verbose_name = "Notifications History"
        verbose_name_plural = "Notifications History"
