from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.v1.users.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, validators=[
        UniqueValidator(queryset=User.with_deleted.all(),
                        message='Already exists username')
    ])
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True, validators=[
        UniqueValidator(queryset=User.with_deleted.all(),
                        message='Already exists email')
    ])
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'password')
