from django.urls import path
from django.urls import include


urlpatterns = [
    path('', include('api.v1.users.urls')),
    path('', include('api.v1.posts.urls')),
]
