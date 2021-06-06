"""Jobs URLs"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jobs.views import JobsViewSet, JobsHistoryViewSet

router = DefaultRouter()
router.register(r'history', JobsHistoryViewSet)
router.register('', JobsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
