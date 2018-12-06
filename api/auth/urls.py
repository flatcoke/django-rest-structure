from django.urls import path, include
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('refresh/', refresh_jwt_token),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
