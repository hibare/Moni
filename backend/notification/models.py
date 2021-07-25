"""Notification models"""

from django.db import models
from moni.utils.funcs import get_str_uuid


class Notifications(models.Model):
    """Notifications"""

    NOTIFICATION_TYPES = [
        ("slack", "Slack"),
        ("discord", "Discord"),
        ("webhook", "Webhook"),
        ("gotify", "Gotify")
    ]

    uuid = models.CharField(
        max_length=40, default=get_str_uuid, primary_key=True)
    url = models.URLField(unique=True)
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    description = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['uuid']),
        ]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"