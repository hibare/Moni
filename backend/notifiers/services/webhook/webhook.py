"""Webhook notification service"""

import logging
from typing import List, Tuple

import requests
from notifiers.services import NotifierService
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class Webhook(NotifierService):
    """Webhook notifiers"""

    def __init__(self) -> None:
        self.payload = {"text": "Moni: Test notification"}
        self.HEADERS = {"Content-type": "application/json"}

    def prep_payload(
        self,
        title: str,
        health_check_url: str,
        success: bool,
        expected_status: List,
        received_status: int,
        error: str | None = None,
    ) -> None:
        self.payload = {
            "title": title,
            "health_check_url": health_check_url,
            "success": success,
            "expected_status": expected_status,
            "received_status": received_status,
            "error": error,
        }

    def send(self, webhook: str) -> Tuple[bool, int | None, str | None]:
        try:
            response = requests.post(webhook, json=self.payload, headers=self.HEADERS)
            response.raise_for_status()
            logger.info(
                "Response from webhook, status_code=%s, response=%s",
                response.status_code,
                response.text,
            )

            return True, response.status_code, None
        except RequestException as err:
            logger.exception("Webhook notification exception")
            return False, None, repr(err)
        except Exception as err:
            logger.exception(
                "An unexpected error occurred while sending Webhook notification: %s",
                err,
            )
            return False, None, repr(err)
