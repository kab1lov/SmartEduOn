from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from apps.courses.models.course import Course
from apps.courses.serializers.course import NewCourseModelSerializer
from apps.users.models import User
from apps.users.models.models import Wishlist
from apps.users.services.cache_functions import getKey, deleteKey
from apps.users.services.email import ActivationEmail
from apps.users.services.validations_errors import Messages
from apps.users.models.models import Basket

error_messages = Messages()


class SendActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": Messages.EMAIL_NOT_FOUND})

        self.context['email'] = email
        ActivationEmail(self.context['request'], self.context).send([email])

        return attrs


class CheckActivationSerializer(serializers.Serializer):
    activation_code = serializers.IntegerField(write_only=True)
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        if getKey(attrs.get('email')) != attrs.get('activation_code'):
            raise serializers.ValidationError({"invalid_code": Messages.INVALID_ACTIVATE_CODE_ERROR})
        deleteKey(attrs.get('email'))
        return attrs


from rest_framework.serializers import SerializerMethodField


class UserModelSerializer(serializers.ModelSerializer):
    course = SerializerMethodField("get_course")

    def get_course(self, obj):
        course = obj.course.all()
        serializer = NewCourseModelSerializer(course, many=True)
        for i in serializer.data:
            i["image"] = "https://infonex.besenior.uz" + i.get("image")
        return serializer.data

    class Meta:
        model = User
        # exclude = ('id', 'last_login', 'is_superuser', 'is_staff', 'created_at', 'updated_at', 'groups',
        #            'user_permissions', 'password')
        fields = (
            'first_name', 'last_name', 'phone', 'image', 'balance', 'email', 'username', 'gender', 'job', 'birthday',
            'about', 'is_active', 'is_spiker', 'course')


class RegisterModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=150)
    re_password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 're_password')

    def check_password(self, **kwargs):
        if kwargs.get("password") != kwargs.get("re_password"):
            raise serializers.ValidationError({"password_mismatch": Messages.PASSWORD_MISMATCH_ERROR})
        return True

    def validate(self, attrs):
        if self.check_password(**attrs):
            attrs.pop('re_password')
            # try:
            #     user = User(**attrs)
            #     validate_password(attrs.get('password'), user)
            # except django_exceptions.ValidationError as e:
            #     serializer_error = serializers.as_serializer_error(e)
            #     raise serializers.ValidationError(
            #         {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            #     )
        attrs['password'] = make_password(attrs.get('password'))
        return attrs


class WishlistModelSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

    def validate(self, attrs):
        user = User.objects.get(id=self.initial_data['user_id'])
        course = Course.objects.get(id=attrs['course_id'])

        if Wishlist.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError({"exists": "Wishlist is already"})
        data = Wishlist.objects.create(user=user, course=course)
        data.save()
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['success'] = 'Wishlist was created successfully'
        return ret

    def create(self, validated_data):
        user_id = self.initial_data['user']
        user = User.objects.get(id=user_id)
        validated_data['user'] = user
        return super().create(validated_data)


class BacketModelSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

    def validate(self, attrs):
        user = User.objects.get(id=self.initial_data['user_id'])
        course = Course.objects.get(id=attrs['course_id'])

        if Wishlist.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError({"exists": "Backet is already"})
        data = Wishlist.objects.create(user=user, course=course)
        data.save()
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['success'] = 'Backet was created successfully'
        return ret

    def create(self, validated_data):
        user_id = self.initial_data['user']
        user = User.objects.get(id=user_id)
        validated_data['user'] = user
        return super().create(validated_data)


class PasswordResetConfirmSerializer(serializers.Serializer):
    activation_code = serializers.IntegerField(write_only=True)
    email = serializers.EmailField(write_only=True)
    new_password = serializers.CharField(max_length=150, write_only=True)
    confirm_password = serializers.CharField(max_length=150, write_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs.get('email'))
            validate_password(attrs.get('new_password'), user)
            validate_password(attrs.get('confirm_password'), user)
        except (User.DoesNotExist, ValidationError) as e:
            raise serializers.ValidationError({"password": str(e)})

        if not self.is_valid_activation_code(attrs['email'], attrs['activation_code']):
            raise serializers.ValidationError({"activation_code": "Invalid activation code"})

        return super().validate(attrs)

    def is_valid_activation_code(self, email, activation_code):
        stored_activation_code = getKey(email)
        if stored_activation_code == activation_code:
            deleteKey(email)
            return True
        return False


class SendEmailResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"email": error_messages.EMAIL_NOT_FOUND})
        user = User.objects.get(email=attrs.get('email'))
        self.context['user'] = user
        ActivationEmail(self.context.get('request'), self.context).send([user.email])
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()
