from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=127)
    email = serializers.EmailField(max_length=127)
    password = serializers.CharField(max_length=127, write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(default=None)
    is_employee = serializers.BooleanField(default=False)

    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data: dict) -> User:
        username = User.objects.filter(
            username__iexact=validated_data["username"]
        ).exists()
        email = User.objects.filter(email__iexact=validated_data["email"]).exists()
        if username and email:
            raise serializers.ValidationError(
                {
                    "email": ["email already registered."],
                    "username": ["username already taken."],
                }
            )
        elif username:
            raise serializers.ValidationError(
                {
                    "username": ["username already taken."],
                }
            )
        elif email:
            raise serializers.ValidationError(
                {
                    "email": ["email already registered."],
                }
            )
        if validated_data["is_employee"]:
            return User.objects.create_superuser(**validated_data)
        return User.objects.create_user(**validated_data)
