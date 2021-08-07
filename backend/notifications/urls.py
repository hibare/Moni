"""Notifications URLs"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notifications.views import NotificationsViewSet, NotificationsHistoryViewSet

router = DefaultRouter()
router.register(r'history', NotificationsHistoryViewSet)
router.register('', NotificationsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
