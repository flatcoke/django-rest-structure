from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.v1.users.models import User
from api.v1.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny, ]
        else:
            permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
        return [permission() for permission in permission_classes]
