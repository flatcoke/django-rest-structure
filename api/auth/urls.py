from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    url(r'^login/$', obtain_jwt_token),
    url(r'^refresh/$', refresh_jwt_token),
]
