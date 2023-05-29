"""Scheduler routines"""

import logging
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import register_events
from django_apscheduler.models import DjangoJobExecution
from jobs.models import JobsHistory
from notifiers.models import NotifiersHistory

logger = logging.getLogger(__name__)

# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def delete_old_job_history(max_age=604800):
    """This job deletes all job history records older than `max_age` from the database."""

    JobsHistory.objects.delete_old_history(max_age)


def delete_old_notifier_history(max_age=604800):
    """This job delete all notifier history older than `max_age` from the database"""

    NotifiersHistory.objects.delete_old_history(max_age)


def start(default_jobs=True):
    """Start Scheduler"""

    if settings.DEBUG:
        # Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    if default_jobs:
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                hour="00", minute="00"
            ),  # Everyday midnight
            id="delete_old_job_executions",
            max_instances=settings.SCHEDULER_JOB_MAX_INSTANCES,
            replace_existing=settings.SCHEDULER_JOB_REPLACE_EXISTING,
            misfire_grace_time=settings.SCHEDULER_JOB_MISFIRE_GRACETIME
        )
        logger.info(
            "Added daily job: 'delete_old_job_executions'."
        )

        scheduler.add_job(
            delete_old_job_history,
            trigger=CronTrigger(
                hour="00", minute="00"
            ),  # Everyday midnight
            id="delete_old_job_history",
            max_instances=settings.SCHEDULER_JOB_MAX_INSTANCES,
            replace_existing=settings.SCHEDULER_JOB_REPLACE_EXISTING,
            misfire_grace_time=settings.SCHEDULER_JOB_MISFIRE_GRACETIME
        )
        logger.info(
            "Added daily job: 'delete_old_job_history'."
        )

        scheduler.add_job(
            delete_old_notifier_history,
            trigger=CronTrigger(
                hour="00", minute="00"
            ),  # Everyday midnight
            id="delete_old_notifier_history",
            max_instances=settings.SCHEDULER_JOB_MAX_INSTANCES,
            replace_existing=settings.SCHEDULER_JOB_REPLACE_EXISTING,
            misfire_grace_time=settings.SCHEDULER_JOB_MISFIRE_GRACETIME
        )
        logger.info(
            "Added daily job: 'delete_old_notifier_history'."
        )

    # Add the scheduled jobs to the Django admin interface
    register_events(scheduler)

    scheduler.start()


def shutdown():
    """Shutdown scheduler"""

    scheduler.shutdown()
