"""Discord notification service"""

import json
import logging
from typing import List, Tuple

import requests
from django.conf import settings
from notifiers.services import NotifierService
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class Discord(NotifierService):
    """Discord notifiers"""

    def __init__(self) -> None:
        self.payload = json.dumps({"content": "Moni: Test notification", "embeds": None}).encode("utf-8")
        self.HEADERS = {"Content-type": "application/json"}
        self.SERVICE_DOWN_TEMPLATE = settings.BASE_DIR / "notifiers/services/discord/template_service_down.json"
        self.SERVICE_UP_TEMPLATE = settings.BASE_DIR / "notifiers/services/discord/template_service_up.json"

    def prep_payload(
        self,
        title: str,
        health_check_url: str,
        success: bool,
        expected_status: List,
        received_status: int,
        error: str | None = None,
    ) -> None:
        TEMPLATE = self.SERVICE_UP_TEMPLATE if success else self.SERVICE_DOWN_TEMPLATE

        with open(TEMPLATE) as ft:
            template_data = ft.read()

        template_data = template_data % (
            title,
            health_check_url,
            expected_status,
            received_status,
            error,
        )

        self.payload = json.loads(template_data)

    def send(self, webhook: str) -> Tuple[bool, int | None, str | None]:
        try:
            response = requests.post(webhook, json=self.payload, headers=self.HEADERS, timeout=10)
            response.raise_for_status()
            logger.info(
                "Response from Discord, status_code=%s, response=%s",
                response.status_code,
                response.text,
            )

            if response.status_code == 204:
                return True, response.status_code, None
            return False, response.status_code, None
        except RequestException as err:
            logger.exception("Failed to send Discord notification, url=%s, error=%s", webhook, err)
            return False, None, repr(err)
        except Exception as err:
            logger.exception(
                "An unexpected error occurred while sending Discord notification: %s",
                err,
            )
            return False, None, repr(err)
