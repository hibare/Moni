"""Notifications admin"""

from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from notification.models import Notifications


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
