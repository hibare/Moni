"""Schedule jobs"""

from django.conf import settings
from django_apscheduler.models import DjangoJobExecution
from jobs.models import Jobs, JobsHistory


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def delete_old_job_history():
    JobsHistory.objects.delete_old_history(settings.JOB_HISTORY_PURGE_AGE)


def update_favicon_url() -> None:
    """Update favicons of all registered jobs"""

    for job in Jobs.objects.all():
        job.update_favicon_url()
