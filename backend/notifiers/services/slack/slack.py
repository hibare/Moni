"""Slack notification service"""

import logging
import json
import requests
from requests.exceptions import RequestException
from typing import List, Tuple
from django.conf import settings
from notifiers.services import NotifierService

logger = logging.getLogger(__name__)


class Slack(NotifierService):
    """Slack notifiers"""

    def __init__(self) -> None:
        self.payload = json.dumps({"text": "Moni: Test notification"}).encode("utf-8")
        self.HEADERS = {"Content-type": "application/json"}
        self.SERVICE_DOWN_TEMPLATE = (
            settings.BASE_DIR / "notifiers/services/slack/template_service_down.json"
        )
        self.SERVICE_UP_TEMPLATE = (
            settings.BASE_DIR / "notifiers/services/slack/template_service_up.json"
        )

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
            health_check_url,
            title,
            expected_status,
            received_status,
            error,
        )

        self.payload = template_data.encode("utf-8")

    def send(self, webhook: str) -> Tuple[bool, int | None, str | None]:
        try:
            response = requests.post(
                webhook,
                json=json.loads(self.payload.decode("utf-8")),
                headers=self.HEADERS,
            )
            response.raise_for_status()
            logger.info(
                "Response from Slack, status_code=%s, response=%s",
                response.status_code,
                response.text,
            )

            if response.status_code == 200:
                return True, response.status_code, None
            return False, response.status_code, None
        except RequestException as err:
            logger.exception("Slack notification exception")
            return False, None, repr(err)
        except Exception as err:
            logger.exception(
                "An unexpected error occurred while sending Slack notification: %s", err
            )
            return False, None, repr(err)
