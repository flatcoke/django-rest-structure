from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import FlogViewSet

app_name = 'flogs'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'', FlogViewSet)

urlpatterns = [
    path('flogs/', include(router.urls)),
]
