"""Telegram notification service"""

import logging
import json
from typing import List, Tuple
from django.conf import settings
from moni.utils.requests_proxy import requests_post
from moni.utils.urls import parse_url
from notifiers.services import NotifierService

logger = logging.getLogger(__name__)


class Telegram(NotifierService):
    """Telegram notifiers"""

    def __init__(self) -> None:
        self.payload = {
            "text": "Moni: Test notification",
            "parse_mode": "HTML"
        }
        self.HEADERS = {
            "Content-type": "application/json"
        }
        self.SERVICE_DOWN_TEMPLATE = settings.BASE_DIR / \
            "notifiers/services/telegram/template_service_down.html"
        self.SERVICE_UP_TEMPLATE = settings.BASE_DIR / \
            "notifiers/services/telegram/template_service_up.html"

    def prep_payload(self, title: str, health_check_url: str, success: bool, expected_status: List, received_status: int, error: str | None = None) -> None:
        TEMPLATE = self.SERVICE_UP_TEMPLATE if success else self.SERVICE_DOWN_TEMPLATE

        with open(TEMPLATE) as ft:
            template_data = ft.read()

        template_data = template_data % (
            health_check_url, title, expected_status, received_status, error)

        self.payload['text'] = template_data

    def send(self, webhook: str) -> Tuple[bool, int | None, str | None]:
        try:
            url_obj = parse_url(webhook)
            chat_id = url_obj.QUERY.get('chat_id')

            if not chat_id:
                raise Exception("Unable to find chat id")

            self.payload['chat_id'] = chat_id
            self.payload = json.dumps(self.payload).encode("utf-8")

            response = requests_post(webhook, self.payload, self.HEADERS)
            logger.info("Response from Telegram, status_code=%s, response=%s",
                        response.status, response.data)

            if response.status == 200:
                return True, response.status, None
            return False, response.status, None
        except Exception as err:
            logger.exception("Telegram notification exception")
            return False, None, repr(err)
