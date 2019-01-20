from rest_framework import serializers
from api.users.serializers import UserSerializer
from api.posts.models import Flog, Comment


class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('user', 'content', 'created_at')


class FlogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Flog
        fields = ('id', 'user', 'title', 'content', 'comments', 'created_at')
