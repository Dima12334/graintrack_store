from rest_framework import serializers as drf_serializers

from graintrack_store.core.api.serializers import BaseProjectModelSerializer
from graintrack_store.users.constants import UserConstants
from graintrack_store.users.models import User


class LoginSerializer(drf_serializers.Serializer):
    username = drf_serializers.CharField(
        required=True, max_length=UserConstants.USERNAME_MAX_LENGTH
    )
    password = drf_serializers.CharField(
        required=True, max_length=UserConstants.PASSWORD_MAX_LENGTH
    )


class UserGetSerializer(BaseProjectModelSerializer):
    uuid = drf_serializers.UUIDField(read_only=True)
    username = drf_serializers.CharField(read_only=True)
    role = drf_serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("uuid", "username", "role")


class LogoutSerializer(drf_serializers.Serializer):
    message = drf_serializers.CharField(read_only=True)
