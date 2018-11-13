from django.conf.urls import url, include
from rest_framework import routers

from .views import UserViewSet

app_name = 'users'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
