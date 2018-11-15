from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.v1.users.models import User
from api.v1.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def list(self, request):
    #     return Response({})

    # def get_permissions(self):
    #     if self.action in ['create']:
    #         permission_classes = [AllowAny, ]
    #     else:
    #         permission_classes = [IsAuthenticated, ]
    #     return [permission() for permission in permission_classes]
