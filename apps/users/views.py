from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404, CreateAPIView, DestroyAPIView, \
    ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.courses.models.course import Course
from apps.users.models import User
from apps.users.models.models import Basket
from apps.users.models.models import Wishlist
from apps.users.serializers.serializers import UserModelSerializer, SendActivationCodeSerializer, \
    CheckActivationSerializer, \
    WishlistModelSerializer, RegisterModelSerializer, SendEmailResetSerializer, PasswordResetConfirmSerializer, \
    BacketModelSerializer, ResetPasswordSerializer, ResetPasswordConfirmSerializer
from apps.users.services.mixins import SendEmailActivationCodeView, CheckActivationCodeView


class EmailActivationView(SendEmailActivationCodeView):
    serializer_class = SendActivationCodeSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [AllowAny]


class CheckActivationView(CheckActivationCodeView):
    serializer_class = CheckActivationSerializer
    parser_classes = (FormParser, MultiPartParser)


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.request.user.pk}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class UserCreateAPIView(CreateAPIView, SendActivationCodeSerializer):
    serializer_class = RegisterModelSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)


class WishlistCreateDestroyAPIView(CreateAPIView, DestroyAPIView, ListAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistModelSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.get('course_id')
        user = request.user
        course = Course.objects.get(id=data)

        if Wishlist.objects.filter(user=user, course=course).exists():
            raise ValidationError({"exists": "Wishlist is already"})
        Wishlist.objects.create(user=user, course=course)
        response = {
            "message": "Courser add"
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {'user': self.request.user.pk}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class BacketCreateDestroyAPIView(CreateAPIView, DestroyAPIView, ListAPIView):
    queryset = Basket.objects.all()
    serializer_class = BacketModelSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.get('course_id')
        user = request.user
        course = Course.objects.get(id=data)

        if Basket.objects.filter(user=user, course=course).exists():
            raise ValidationError({"exists": "Backet is already"})
        Basket.objects.create(user=user, course=course)
        response = {
            "message": "Courser add"
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {'user': self.request.user.pk}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class PasswordResetGenericAPIView(GenericAPIView):
    serializer_class = SendEmailResetSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        # return Response({'email': email}, status=status.HTTP_200_OK)
        return Response({'message': 'Reset Password successfully send.'}, status=status.HTTP_200_OK)


class PasswordResetConfirmUpdateAPIView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('new_password')
        user = User.objects.get(email=serializer.validated_data.get('email'))
        user.password = make_password(password)
        user.save(update_fields=["password"])
        return Response(status=status.HTTP_200_OK)

from django.utils.crypto import get_random_string
from django.core.mail import send_mail
import random
class ResetPasswordView(CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User not found with this email."}, status=status.HTTP_400_BAD_REQUEST)

            activation_code = str(random.randint(100000, 999999))  # Generate a random 6-digit code
            user.set_password(activation_code)
            user.save()

            send_mail(
                'Password Reset Confirmation',
                f'Your password reset code is: {activation_code}',
                'admin@example.com',
                [email],
                fail_silently=False,
            )

            return Response({"detail": "Password reset code sent to your email."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmView(CreateAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            activation_code = serializer.validated_data['activation_code']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User not found with this email."}, status=status.HTTP_400_BAD_REQUEST)

            if user.check_password(activation_code):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "New password and confirm password do not match."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Invalid activation code."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

