"""Notification service"""


import logging
from typing import List
from notification.models import Notifications

logger = logging.getLogger(__name__)


class Notify:
    """Notification handlers"""

    def __init__(self) -> None:
        pass

    def notify(self, urls: List[Notifications], title: str, body: str = None):
        """Notify"""

        pass
