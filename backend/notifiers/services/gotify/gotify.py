"""Gotify notification service"""

import logging
import json
from typing import List, Tuple
from django.conf import settings
from moni.requests.proxy import requests_post
from notifiers.services import NotifierService


logger = logging.getLogger(__name__)


class Gotify(NotifierService):
    """Gotify notifiers"""

    def __init__(self) -> None:
        self.payload = json.dumps({
            "title": "Moni: Test notification",
            "message": "Test Message"
        }).encode("utf-8")
        self.HEADERS = {
            "Content-type": "application/json"
        }
        self.SERVICE_DOWN_TEMPLATE = settings.BASE_DIR / \
            "notifiers/services/gotify/template_service_down.json"
        self.SERVICE_UP_TEMPLATE = settings.BASE_DIR / \
            "notifiers/services/gotify/template_service_up.json"

    def prep_payload(self, title: str, health_check_url: str, success: bool, expected_status: List, received_status: int, error: str | None = None) -> None:
        TEMPLATE = self.SERVICE_UP_TEMPLATE if success else self.SERVICE_DOWN_TEMPLATE

        with open(TEMPLATE) as ft:
            template_data = ft.read()

        template_data = template_data % (
            title, health_check_url, expected_status, received_status, error)

        self.payload = template_data.encode("utf-8")

    def send(self, webhook: str) -> Tuple[bool, int | None, str | None]:
        try:
            response = requests_post(webhook, self.payload, self.HEADERS)
            logger.info("Response from Gotify, status_code=%s, response=%s",
                        response.status, response.data)

            if response.status == 200:
                return True, response.status, None
            return False, response.status, None
        except Exception as err:
            logger.exception("Gotify notification exception")
            return False, None, repr(err)
