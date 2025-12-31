from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now


from .models import User, PasswordResetToken
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            token = get_random_string(48)
            PasswordResetToken.objects.create(user=user, token=token)

            reset_link = (
                f"{settings.FRONTEND_URL}/reset-password?token={token}"
            )

            html_message = render_to_string(
                    "emails/reset_password.html",
                    {
                        "reset_link": reset_link,
                        "year": now().year,
                    }
            )

            plain_message = strip_tags(html_message)

            send_mail(
                    subject="Reset your Noir Élixir password",
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    html_message=html_message,
            )


            return Response(
                {"message": "Password reset link sent"},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data["token"]
            password = serializer.validated_data["password"]

            try:
                reset_obj = PasswordResetToken.objects.get(token=token)
            except PasswordResetToken.DoesNotExist:
                return Response(
                    {"error": "Invalid or expired token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ⏱️ TOKEN EXPIRY (15 MINUTES)
            if reset_obj.created_at < timezone.now() - timedelta(minutes=15):
                reset_obj.delete()
                return Response(
                    {"error": "Reset link expired"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = reset_obj.user
            user.set_password(password)
            user.save()

            reset_obj.delete()

            return Response(
                {"message": "Password reset successful"},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
