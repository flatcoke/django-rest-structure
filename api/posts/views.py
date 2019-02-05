from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly


class FlogViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all() \
        .select_related('user') \
        .prefetch_related('comments__user')
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
