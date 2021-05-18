"""Jobs Signals"""

import logging
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from jobs.models import Jobs
from jobs.job_operations import JobOps

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Jobs)
def job_post_save(sender, instance, created, **kwargs):
    logger.info("Instance=%s, created=%s", instance, created)

    if created:
        JobOps.add(instance.uuid)
    else:
        if instance.tracker.has_changed('state'):
            if instance.state:
                JobOps.resume(instance.uuid)
            else:
                JobOps.pause(instance.uuid)

        if instance.tracker.has_changed('interval'):
            JobOps.reschedule(instance.uuid, instance.interval)


@receiver(post_delete, sender=Jobs)
def job_post_delete(sender, instance, **kwargs):
    logger.info("Instance=%s", instance)
    JobOps.remove(instance.uuid)
