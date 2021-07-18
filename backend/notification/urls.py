"""Notification URLs"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notification.views import NotificationViewSet

router = DefaultRouter()
router.register('', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls))
]
