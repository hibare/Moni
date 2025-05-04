"""Controller URLs"""

from django.urls import path
from controller.views import JobsControllerViewSet

urlpatterns = [
    path(
        "jobs/misfire/gracetime/",
        JobsControllerViewSet.as_view({"post": "update_misfire_grace_time"}),
        name="Jobs misfire gracetime update",
    ),
    path(
        "jobs/misfire/gracetime/<str:uuid>/",
        JobsControllerViewSet.as_view({"post": "update_misfire_grace_time"}),
        name="Jobs misfire gracetime update",
    ),
]
