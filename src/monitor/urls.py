from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/statuscheck/', include('celerybeat_status.urls')),
    path('', views.index, name="Index_view"),
    path('__health', views.health_check, name="Health_check_view"),
    path('__ping', views.ping, name="Ping_view")
]
