from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import (EmailActivationView, CheckActivationView, UserRetrieveUpdateDestroyAPIView,
                              UserCreateAPIView, ResetPasswordView, ResetPasswordConfirmView)
from apps.users.views import PasswordResetGenericAPIView, PasswordResetConfirmUpdateAPIView

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('send-email', EmailActivationView.as_view(), name='send_email'),
    path('check-activate-code', CheckActivationView.as_view(), name='check_activate_code'),
    path('me', UserRetrieveUpdateDestroyAPIView.as_view(), name='me'),
    path('register', UserCreateAPIView.as_view(), name='register'),
    # path('wishlist', WishlistCreateDestroyAPIView.as_view(), name='wishlist'),

    # path('reset-passwd', PasswordResetGenericAPIView.as_view(), name='reset_passwd'),
    # path('reset-passwd-confirm', PasswordResetConfirmUpdateAPIView.as_view(), name='reset_passwd_confirm'),

    path('api/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('api/reset-password-confirm/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),

    # path('basket', BacketCreateDestroyAPIView.as_view(), name='basket'),

]

