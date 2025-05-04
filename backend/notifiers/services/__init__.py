
from typing import Any, List, Tuple
from abc import ABC, abstractmethod
from django.conf import settings


class NotifierService(ABC):
    """
        Notifier service abstract class
    """

    payload: Any
    DefaultHeaders: dict[str, str] = {
		"Cache-Control": "no-cache",
		"User-Agent": settings.MONI_USER_AGENT
	}

    @abstractmethod
    def prep_payload(self, title: str, health_check_url: str, success: bool, expected_status: List, received_status: int, error: str | None = None) -> None:
        pass

    @abstractmethod
    def send(self, webhook: str) -> Tuple[bool, int | None, str | None]:
        pass
