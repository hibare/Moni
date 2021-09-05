"""Job Operations"""

import time
import ssl
import logging
from typing import Dict, Tuple, Union
import urllib3
from jobs.models import Jobs, JobsHistory
from jobs.scheduler import scheduler
from notifiers.services.notify import Notify

logger = logging.getLogger(__name__)


def request(url: str, headers: Dict = dict, verify_ssl: bool = True, check_redirect: bool = True) -> Tuple[Union[int, None], Union[str, None], Union[float, None]]:
    """
    HTTP Request executor

    Return: HTTP status, response data, time elapsed
    """

    DEFAULT_HEADERS = {
        "Cache-Control": "no-cache"
    }

    headers.update(DEFAULT_HEADERS)

    try:
        if verify_ssl:
            cert_reqs = ssl.CERT_REQUIRED
        else:
            cert_reqs = ssl.CERT_NONE

        http = urllib3.PoolManager(cert_reqs=cert_reqs)

        start = time.time()
        response = http.request(
            'GET',
            url,
            headers=headers,
            timeout=10,
            redirect=check_redirect
        )
        end = time.time()

        elapsed_seconds = end - start

        return response.status, response.data.decode(), elapsed_seconds, None

    except UnicodeDecodeError as e:
        return response.status, response.data, None, str(e)

    except Exception as err:
        logger.exception("URL=%s", url)
        return None, None, None, str(err)


def executor(id: str) -> None:
    """Healthcheck executor"""

    logger.info("Running health check, id=%s", id)

    try:
        job = Jobs.objects.get(uuid=id)

        title = job.title
        url = job.url
        headers = job.headers
        verify_ssl = job.verify_ssl
        success_status = job.success_status
        check_redirect = job.check_redirect
        notifiers = job.notifiers.all()

        status_code, response, elapsed_seconds, error = request(
            url, headers, verify_ssl, check_redirect)

        success = (status_code in success_status) and error is None

        logger.info("Response id=%s, url=%s, status_code=%s, elapsed_seconds=%s, success=%s, error=%s",
                    id, url, status_code, elapsed_seconds, success, error)

        # Notify failure
        if notifiers and not success:
            for notifier in notifiers:
                Notify.notify(notifier, title, url,
                              success, success_status, status_code, error)

        # Record job execution history
        _ = JobsHistory.objects.create(
            uuid=job,
            status_code=status_code,
            success=success,
            response_time=elapsed_seconds,
            error=error
        )

    except Exception:
        logger.exception("Failed to execute healthcheck, id=%s", id)

        # Todo - Notify failure


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
            logger.info("Job added, id=%s", id)
            return True
        except Exception:
            logger.exception("Failed to add new job, id=%s", id)
            return False

    @staticmethod
    def remove(id: str) -> bool:
        """Remove an existing job"""

        try:
            scheduler.remove_job(id)
            logger.info("Job removed, id=%s", id)
            return True

        except Exception:
            logger.exception("Failed to remove job, id=%s", id)
            return False

    @staticmethod
    def pause(id: str) -> bool:
        """Pause a job"""

        try:
            scheduler.pause_job(id)
            logger.info("Job paused, id=%s", id)
            return True
        except Exception:
            logger.exception("Failed to pause job, id=%s", id)
            return False

    @staticmethod
    def resume(id: str) -> bool:
        """Resume a job"""

        try:
            scheduler.resume_job(id)
            logger.info("Job resumed, id=%s", id)
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
            logger.info("Job rescheduled, id=%s", id)
            return True
        except Exception:
            logger.exception("Failed to reschedule job, id=%s", id)
            return False
