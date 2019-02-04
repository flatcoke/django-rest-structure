from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.posts.models import Post
from api.posts.serializers import FlogSerializer


class FlogViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all() \
        .select_related('user') \
        .prefetch_related('comments__user')
    serializer_class = FlogSerializer

    permission_classes = (IsAuthenticated,)
