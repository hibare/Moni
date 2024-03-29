"""Jobs App Config"""

from django.apps import AppConfig
from django.conf import settings


class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'

    def ready(self):
        import jobs.signals
