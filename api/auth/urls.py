from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^token/', obtain_jwt_token),
    url(r'', include('rest_framework.urls', namespace='rest_framework'))
]
