"""Schedule jobs"""

from django_apscheduler.models import DjangoJobExecution
from django.conf import settings
from jobs.models import JobsHistory


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` (in seconds) from the database."""

    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def delete_old_job_history():
    """This job deletes all job history records older than `settings.JOB_HISTORY_PURGE_AGE` (in days) from the database."""

    JobsHistory.objects.delete_old_history(settings.JOB_HISTORY_PURGE_AGE)
