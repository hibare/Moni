"""Jobs URLs"""

from django.urls import include, path
from jobs.views import JobsHistoryViewSet, JobsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"history", JobsHistoryViewSet)
router.register("", JobsViewSet)

urlpatterns = [path("", include(router.urls))]
