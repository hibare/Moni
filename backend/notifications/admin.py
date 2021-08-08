"""Notifications admin"""

from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from notifications.models import Notifications, NotificationsHistory


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    """Notifications admin class"""

    empty_value_display = '-empty-'
    list_display = ['uuid', 'url', 'type',
                    'description']
    list_filter = ['type']

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Optional[Notifications] = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Optional[Notifications] = None) -> bool:
        return False


@admin.register(NotificationsHistory)
class NotificationsHistoryAdmin(admin.ModelAdmin):
    """Notifications admin class"""

    empty_value_display = '-empty-'
    list_display = ['timestamp', 'uuid', 'status', 'status_code', 'error']
    list_filter = ['uuid', 'status_code']

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Optional[Notifications] = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Optional[Notifications] = None) -> bool:
        return False
