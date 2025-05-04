"""Jobs controller functionality"""

import logging
from django_apscheduler.models import DjangoJob
import pickle
from moni.scheduler import scheduler
from jobs.models import Jobs

logger = logging.getLogger(__name__)


class JobsController:
    @classmethod
    def update_job_misfire_grace_time(cls, uuid: str, grace_time: int) -> None:
        job = DjangoJob.objects.get(id=uuid)
        job_state = pickle.loads(job.job_state)
        job_state["misfire_grace_time"] = grace_time
        job.job_state = pickle.dumps(job_state)
        job.save()
        logger.info("Job misfire grace time updated, id=%s", uuid)

    @classmethod
    def update_jobs_misfire_grace_time(cls, grace_time: int) -> None:
        jobs = DjangoJob.objects.all()

        for job in jobs:
            cls.update_job_misfire_grace_time(job.id, grace_time)

    @classmethod
    def pause_jobs(cls) -> None:
        jobs = Jobs.objects.all()

        for job in jobs:
            scheduler.pause_job(job.uuid)
            logger.info("Job paused, id=%s", job.uuid)

    @classmethod
    def resume_jobs(cls) -> None:
        jobs = Jobs.objects.all()

        for job in jobs:
            scheduler.resume_job(job.uuid)
            logger.info("Job resumed, id=%s", job.uuid)
