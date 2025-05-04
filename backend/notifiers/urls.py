"""Notifiers URLs"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notifiers.views import NotifiersViewSet, NotifiersHistoryViewSet

router = DefaultRouter()
router.register(r"history", NotifiersHistoryViewSet)
router.register("", NotifiersViewSet)

urlpatterns = [path("", include(router.urls))]
