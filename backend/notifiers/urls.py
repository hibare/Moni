"""Notifiers URLs"""

from django.urls import include, path
from notifiers.views import NotifiersHistoryViewSet, NotifiersViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"history", NotifiersHistoryViewSet)
router.register("", NotifiersViewSet)

urlpatterns = [path("", include(router.urls))]
