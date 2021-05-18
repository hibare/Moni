"""Jobs admin"""

from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from jobs.models import Jobs


@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    """Job admin class"""

    empty_value_display = '-empty-'
    list_display = ['uuid', 'url', 'title',
                    'state', 'notify_url', 'verify_ssl', 'interval']
    list_filter = ['state', 'verify_ssl', 'interval']

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Optional[Jobs] = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Optional[Jobs] = None) -> bool:
        return False