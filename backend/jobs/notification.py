"""Notification service based on apprise"""


import logging
from typing import List
import apprise

logger = logging.getLogger(__name__)


class Notification:
    """Notification handlers"""

    def __init__(self) -> None:
        pass

    def notify(self, urls: List[str], title: str, body: str = None):
        """Notify"""

        apobj = apprise.Apprise()

        for url in urls:
            apobj.add(url)

        apobj.notify(
            title=title,
            body=body
        )
