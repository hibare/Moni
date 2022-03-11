"""moni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from .views import index_v, health_v, version_v, OpenAPISchemaView, ReDocView, SwaggerUIView

urlpatterns = [
    path('', index_v, name='index'),
    path('favicon.ico/', RedirectView.as_view(
        url='/static/img/favicon.ico',
        permanent=True
    ), name='favicon'),
    path('favicon-fail.ico/', RedirectView.as_view(
        url='/static/img/favicon-fail.ico',
        permanent=True
    ), name='favicon'),
    path('admin/', admin.site.urls),
    path('__version/', version_v, name='version'),
    path('__health/', health_v, name='health'),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/jobs/', include('jobs.urls')),
    path('api/v1/notifiers/', include('notifiers.urls')),
    path('openapi/', OpenAPISchemaView.as_view(), name='openapi-schema'),
    path('redoc/', ReDocView.as_view(), name='redoc'),
    path('swagger/', SwaggerUIView.as_view(), name='swagger-ui'),
]
