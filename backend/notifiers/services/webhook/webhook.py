"""Webhook notification service"""

import logging
from typing import List, Tuple
import json
from moni.requests.proxy import requests_post
from notifiers.services import NotifierService


logger = logging.getLogger(__name__)


class Webhook(NotifierService):
    """Webhook notifiers"""

    def __init__(self) -> None:
        self.payload = json.dumps({
            "text": "Moni: Test notification"
        }).encode("utf-8")
        self.HEADERS = {
            "Content-type": "application/json"
        }

    def prep_payload(self, title: str, health_check_url: str, success: bool, expected_status: List, received_status: int, error: str | None = None) -> None:
        payload = {
            "title": title,
            "health_check_url": health_check_url,
            "success": success,
            "expected_status": expected_status,
            "received_status": received_status,
            "error": error
        }

        self.payload = json.dumps(payload).encode("utf-8")

    def send(self, webhook: str) -> Tuple[bool, int | None, str | None]:
        try:
            response = requests_post(webhook, self.payload, self.HEADERS)
            logger.info("Response from webhook, status_code=%s, response=%s",
                        response.status, response.data)

            if response.status == 200:
                return True, response.status, None
            return False, response.status, None
        except Exception as err:
            logger.exception("Webhook notification exception")
            return False, None, repr(err)
