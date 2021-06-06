"""Job Operations"""


import ssl
import logging
from typing import Tuple, Union
import urllib3
from jobs.models import Jobs
from jobs.scheduler import scheduler
from jobs.notification import Notification

logger = logging.getLogger(__name__)


def request(url: str, verify_ssl: bool = True, check_redirect: bool = True) -> Tuple[Union[int, None], Union[str, None]]:
    """HTTP Request executor"""

    try:
        if verify_ssl:
            cert_reqs = ssl.CERT_REQUIRED
        else:
            cert_reqs = ssl.CERT_NONE

        http = urllib3.PoolManager(cert_reqs=cert_reqs)

        response = http.request(
            'GET',
            url,
            timeout=10,
            redirect=check_redirect
        )

        return response.status, response.data.decode()
    except Exception:
        return None, None


def executor(id: str) -> None:
    """Healthcheck executor"""

    logger.info("Runnin health check, id=%s", id)

    try:
        job = Jobs.objects.get(uuid=id)
        title = job.title
        url = job.url
        verify_ssl = job.verify_ssl
        success_status = job.success_status
        check_redirect = job.check_redirect
        notify_url = job.notify_url

        status, data = request(url, verify_ssl, check_redirect)
        logger.info("Response id=%s, url=%s, status=%s, data=%s",
                    id, url, status, data)

        if status != success_status and notify_url:
            # Notify failure
            Notification().notify(
                [notify_url],
                "Service %s down" % (title),
                "\nSuccess status: %s \nStatus received: %s \nResponse: %s" % (
                    success_status, status, data, )
            )

    except Exception:
        logger.exception("Failed to execute healthcheck, id=%s", id)

        # Notify failure


class JobOps:
    """Job operations"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def add(id: str) -> bool:
        """Add a new job"""

        try:
            job = Jobs.objects.get(uuid=id)
            interval = job.interval
            scheduler.add_job(
                executor,
                "interval",
                id=id,
                minutes=interval,
                args=[id]
            )
            return True
        except Exception:
            logger.exception("Failed to add new job, id=%s", id)
            return False

    @staticmethod
    def remove(id: str) -> bool:
        """Remove an existing job"""

        try:
            scheduler.remove_job(id)
            return True
        except Exception:
            logger.exception("Failed to remove job, id=%s", id)
            return False

    @staticmethod
    def pause(id: str) -> bool:
        """Pause a job"""

        try:
            scheduler.pause_job(id)
            return True
        except Exception:
            logger.exception("Failed to pause job, id=%s", id)
            return False

    @staticmethod
    def resume(id: str) -> bool:
        """Resume a job"""

        try:
            scheduler.resume_job(id)
            return True
        except Exception:
            logger.exception("Failed to resume job, id=%s", id)
            return False

    @staticmethod
    def reschedule(id: str, interval: int) -> bool:
        """Reschedule a job"""

        try:
            scheduler.reschedule_job(id,
                                     jobstore=None, trigger="interval", minutes=interval)
            return True
        except Exception:
            logger.exception("Failed to reschedule job, id=%s", id)
            return False
