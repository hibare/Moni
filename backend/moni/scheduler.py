"""Scheduler routines"""

import logging
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import register_events
from jobs.scheduler import delete_old_job_executions, delete_old_job_history
from notifiers.scheduler import delete_old_notifier_history

logger = logging.getLogger(__name__)

# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


def start(default_jobs=True):
    """Start Scheduler"""

    if settings.DEBUG:
        # Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # Add the scheduled jobs to the Django admin interface
    register_events(scheduler)

    scheduler.start()

    default_jobs_func = {
        "delete_old_job_executions": {
            "func": delete_old_job_executions,
            "trigger": CronTrigger(
                hour="00", minute="00"
            )
        },
        "delete_old_job_history": {
            "func": delete_old_job_history,
            "trigger": CronTrigger(
                hour="00", minute="00"
            )
        },
        "delete_old_notifier_history": {
            "func": delete_old_notifier_history,
            "trigger": CronTrigger(
                hour="00", minute="00"
            )
        }
    }

    if default_jobs:
        for id, det in default_jobs_func.items():
            scheduler.add_job(
                det['func'],
                trigger=det['trigger'],
                id=id,
                max_instances=settings.SCHEDULER_JOB_MAX_INSTANCES,
                replace_existing=settings.SCHEDULER_JOB_REPLACE_EXISTING,
                misfire_grace_time=settings.SCHEDULER_JOB_MISFIRE_GRACETIME
            )
            logger.info("Added daily job: '%s'.", id)


def shutdown():
    """Shutdown scheduler"""

    scheduler.shutdown()
