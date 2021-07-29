"""Moni Views"""

import logging
import yaml
from django.http import JsonResponse
from django.conf import settings
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import permissions

logger = logging.getLogger(__name__)


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


class OpenAPISchemaView(APIView):
    """
    Return OpenAPI Schema

    application/vnd.oai.openapi
    """

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.JSONOpenAPIRenderer,
        renderers.BrowsableAPIRenderer
    ]

    def get(self, request, format=None):
        """
        Return OpenAPI Schema. 
        """
        schema_file = "moni/openapi-schema.yml"

        schema_file_path = settings.BASE_DIR / schema_file

        with open(schema_file_path) as stream:
            data = yaml.safe_load(stream)

        # Update app info
        data['info']['version'] = settings.VERSION
        data['info']['title'] = settings.TITLE

        return Response(data)


class ReDocView(APIView):
    """
    Handle ReDoc request
    """

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    renderer_classes = [
        renderers.TemplateHTMLRenderer
    ]

    def get(self, request):
        """
        Return ReDoc template. 
        """

        return Response({'schema_url': 'openapi-schema'}, template_name='moni/redoc.html')


class SwaggerUIView(APIView):
    """
    Handle SwaggerUI request
    """

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    renderer_classes = [
        renderers.TemplateHTMLRenderer
    ]

    def get(self, request):
        """
        Return ReDoc template. 
        """

        return Response({'schema_url': 'openapi-schema'}, template_name='moni/swagger-ui.html')
