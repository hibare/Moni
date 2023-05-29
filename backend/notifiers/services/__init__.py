
from typing import Any, List, Tuple
from abc import ABC, abstractmethod


class NotifierService(ABC):
    """
        Notifier service abstract class
    """

    payload: Any

    @abstractmethod
    def prep_payload(self, title: str, health_check_url: str, success: bool, expected_status: List, received_status: int, error: str | None = None) -> None:
        pass

    @abstractmethod
    def send(self, webhook: str) -> Tuple[bool, int | None, str | None]:
        pass
