"""Jobs Signals"""

import logging
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from jobs.models import Jobs
from jobs.operations import JobOps
from moni.utils.favicon import Favicon

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Jobs)
def job_post_save(sender, instance, created, **kwargs):
    """
    Create Job when a new job entry is made & update favicon URL.
    Update scheduled job when job record is updated.
    When state is changed:
        state=True, set job status active, resume job
        state=False, set job status inactive, pause job
    When internval changed, reschedule job
    """

    if created:
        JobOps.add(instance.uuid)
        instance.update_favicon_url()
    else:
        if instance.tracker.has_changed('state'):
            if instance.state:
                JobOps.resume(instance.uuid)
            else:
                JobOps.pause(instance.uuid)

        if instance.tracker.has_changed('interval'):
            JobOps.reschedule(instance.uuid, instance.interval)

    if instance.state and (created or instance.tracker.has_changed('state') or instance.tracker.has_changed('url')):
        JobOps.run(instance.uuid)


@receiver(post_delete, sender=Jobs)
def job_post_delete(sender, instance, **kwargs):
    """Delete scheduled job when the job record is deleted"""

    JobOps.remove(instance.uuid)
