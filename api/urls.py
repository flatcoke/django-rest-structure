from django.urls import include, path

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('v1/', include('api.v1.urls')),
]
