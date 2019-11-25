from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="Index_view"),
    path('__health', views.health_check, name="Health_check_view"),
    path('__ping', views.ping, name="Ping_view")
]
