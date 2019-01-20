from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import UserViewSet

app_name = 'users'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
