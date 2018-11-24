from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.v1.posts.models import Flog
from api.v1.posts.serializers import FlogSerializer


class FlogViewSet(viewsets.ModelViewSet):
    queryset = Flog.objects.all().prefetch_related('comments__user')
    serializer_class = FlogSerializer

    permission_classes = (IsAuthenticated,)
