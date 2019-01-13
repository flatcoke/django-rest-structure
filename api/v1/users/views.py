from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from api.v1.users.models import User
from api.v1.users.permissions import IsOwnerOrReadOnly
from api.v1.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id').cache()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny, ]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
