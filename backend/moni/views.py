"""Moni Views"""

from django.http import JsonResponse
from django.conf import settings


def health_v(request):
    """Health view"""

    return JsonResponse({
        "status": "healthy"
    })


def version_v(request):
    """Version view"""

    return JsonResponse({
        "version": settings.VERSION
    })
