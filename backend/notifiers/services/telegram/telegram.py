"""Telegram notification service"""

import logging
from typing import List, Tuple

import requests
from django.conf import settings
from moni.requests.urls import parse_url
from notifiers.services import NotifierService
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class Telegram(NotifierService):
    """Telegram notifiers"""

    def __init__(self) -> None:
        self.payload = {"text": "Moni: Test notification", "parse_mode": "HTML"}
        self.HEADERS = {"Content-type": "application/json"}
        self.SERVICE_DOWN_TEMPLATE = settings.BASE_DIR / "notifiers/services/telegram/template_service_down.html"
        self.SERVICE_UP_TEMPLATE = settings.BASE_DIR / "notifiers/services/telegram/template_service_up.html"

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

        self.payload["text"] = template_data

    def send(self, webhook: str) -> Tuple[bool, int | None, str | None]:
        try:
            url_obj = parse_url(webhook)
            chat_id = url_obj.QUERY.get("chat_id")

            if not chat_id:
                raise Exception("Unable to find chat id")

            self.payload["chat_id"] = chat_id

            response = requests.post(webhook, json=self.payload, headers=self.HEADERS)
            logger.info(
                "Response from Telegram, status_code=%s, response=%s",
                response.status_code,
                response.text,
            )

            if response.status_code == 200:
                return True, response.status_code, None
            return False, response.status_code, None
        except RequestException as e:
            logger.exception("Failed to send Telegram notification, webhook=%s, error=%s", webhook, e)
            return False, None, repr(e)
        except Exception as err:
            logger.exception(
                "An unexpected error occurred while sending Telegram notification: %s",
                err,
            )
            return False, None, repr(err)
