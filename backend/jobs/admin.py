"""Jobs admin"""

from typing import Optional

from django.contrib import admin
from django.http.request import HttpRequest
from jobs.models import Jobs, JobsHistory


@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    """Job admin class"""

    empty_value_display = "-empty-"
    list_display = [
        "uuid",
        "url",
        "title",
        "healthy",
        "state",
        "verify_ssl",
        "interval",
        "favicon_url",
        "check_redirect",
        "success_status",
        "headers",
        "failure_threshold",
    ]
    list_filter = ["state", "verify_ssl", "interval", "healthy", "check_redirect"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Optional[Jobs] = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Optional[Jobs] = None) -> bool:
        return False


@admin.register(JobsHistory)
class JobsHistoryAdmin(admin.ModelAdmin):
    """Jobs History admin class"""

    empty_value_display = "-empty-"
    list_display = [
        "timestamp",
        "uuid",
        "status_code",
        "success",
        "response_time",
        "error",
    ]
    list_filter = ["timestamp", "uuid", "status_code", "success"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Optional[Jobs] = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Optional[Jobs] = None) -> bool:
        return True
