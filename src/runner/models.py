from django.db import models


class Monitors(models.Model):
    health_check_url = models.CharField(max_length=5000)
    mail_recipient = models.CharField(
        max_length=200, null=True, blank=True)
    slack_endpoint = models.CharField(max_length=5000, null=True, blank=True)
    description = models.CharField(max_length=2000)
    active = models.BooleanField(default=True)
