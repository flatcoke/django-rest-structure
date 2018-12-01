from django.urls import path, include

urlpatterns = [
    path('', include('api.v1.users.urls')),
    path('', include('api.v1.posts.urls')),
]
