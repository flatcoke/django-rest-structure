from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url(r'^users/', include('api.v1.users.urls')),
]
