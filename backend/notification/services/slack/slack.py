"""Slack notification service"""

import logging
import json
from typing import List
from django.conf import settings
from moni.utils.requests_proxy import requests_post

logger = logging.getLogger(__name__)


class Slack:
    """Slack notifications"""

    def __init__(self) -> None:
        self.payload = json.dumps({
            "text": "Moni: Test notification"
        }).encode("utf-8")
        self.HEADERS = {
            "Content-type": "application/json"
        }
        self.SERVICE_DOWN_TEMPLATE = settings.BASE_DIR / \
            "notification/services/slack/template_service_down.json"
        self.SERVICE_UP_TEMPLATE = settings.BASE_DIR / \
            "notification/services/slack/template_service_up.json"

    def prep_payload(self, title: str, health_check_url: str, success: bool, expected_status: List, received_status: int, error: str = None) -> None:
        TEMPLATE = self.SERVICE_UP_TEMPLATE if success else self.SERVICE_DOWN_TEMPLATE

        with open(TEMPLATE) as ft:
            template_data = ft.read()

        template_data = template_data % (
            health_check_url, title, expected_status, received_status, error)

        self.payload = template_data.encode("utf-8")

    def send(self, webhook: str) -> bool:
        try:
            response = requests_post(webhook, self.payload, self.HEADERS)
            logger.debug("Response from Slack, status_code=%s, response=%s",
                         response.status, response.data)

            if response.status == 200:
                return True
            return False
        except Exception:
            logger.exception("Slack notification exception")
            return False