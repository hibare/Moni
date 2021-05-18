"""Moni Views"""

from django.http import JsonResponse


def health_v(requets):
    """Health view"""

    return JsonResponse({
        "status": "healthy"
    })
