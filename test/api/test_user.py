import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.services.cache_functions import getKey


@pytest.mark.django_db
class TestActivationUserGenericAPIView:
    activation_code = ''
    client = APIClient()
    payload = dict(
        first_name="Qobilov",
        last_name="Abror",
        username="xo'ja",
        password="b2002234",
        re_password="b2002234",
        email="inagamovzaynobiddin@gmail.com"

    )

    urls = {
        'send_email': reverse('send_email'),
        'register': reverse('register'),
        'activate': reverse('check_activate_code'),
        'reset_password': reverse('reset_passwd'),
        'reset_password_confirm': reverse('reset_passwd_confirm')

    }

    @pytest.fixture
    def test_send_activation_code(self):
        data = {
            'email': self.payload.get('email')
        }
        response = self.client.post(self.urls.get('send_email'), data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.fixture
    def test_user_register(self):
        response = self.client.post(self.urls.get('register'), self.payload)

        data = response.data
        assert response.status_code == status.HTTP_201_CREATED
        assert data["email"] == self.payload["email"]

    def test_user_activation(self, test_user_register):
        data = {
            'email': self.payload.get('email'),
            'activation_code': getKey(self.payload.get('email'))
        }
        response = self.client.post(self.urls.get('activate'), data)
        assert response.status_code == status.HTTP_200_OK

    def test_user_activation_invalid_data(self):
        data = {'email': 'invalid-email'}
        response = self.client.post(self.urls.get('activate'), data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
