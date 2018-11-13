from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.v1.users.models import User
from api.v1.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    # permission_classes = ()

    queryset = User.objects.all()
    serializer_class = UserSerializer
