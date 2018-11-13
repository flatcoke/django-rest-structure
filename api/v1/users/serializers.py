from rest_framework import serializers
from api.v1.users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        user.save()
        return user
