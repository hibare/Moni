"""Notifiers admin"""

from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from notifiers.models import Notifiers, NotifiersHistory


@admin.register(Notifiers)
class NotifiersAdmin(admin.ModelAdmin):
    """Notifiers admin class"""

    empty_value_display = "-empty-"
    list_display = ["uuid", "state", "url", "type", "description"]
    list_filter = ["type", "state"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[Notifiers] = None
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[Notifiers] = None
    ) -> bool:
        return False


@admin.register(NotifiersHistory)
class NotifiersHistoryAdmin(admin.ModelAdmin):
    """Notifiers admin class"""

    empty_value_display = "-empty-"
    list_display = ["timestamp", "uuid", "status", "status_code", "error"]
    list_filter = ["uuid", "status_code"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[Notifiers] = None
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[Notifiers] = None
    ) -> bool:
        return False
