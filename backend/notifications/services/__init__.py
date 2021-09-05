
from typing import List
from abc import ABC, abstractmethod


class NotificationService(ABC):
    """
        Notification service abstract class
    """

    @abstractmethod
    def prep_payload(self, title: str, health_check_url: str, success: bool, expected_status: List, received_status: int, error: str = None) -> None:
        pass

    @abstractmethod
    def send(self, webhook: str) -> bool:
        pass
