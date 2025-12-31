from rest_framework import serializers
from .models import User, PasswordResetToken
from django.utils import timezone
from datetime import timedelta


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "first_name",
            "last_name",
        ]
        read_only_fields = ["id", "username", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        email = validated_data["email"]

        user = User.objects.create_user(
            username=email.split("@")[0],
            email=email,
            password=validated_data["password"],
        )
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "User with this email does not exist"
            )
        return email


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=6)
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
