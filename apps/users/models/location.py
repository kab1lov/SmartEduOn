from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class Region(models.Model):
    name = models.CharField(_("name"), max_length=150)

class District(models.Model):
    name = models.CharField(_("name"), max_length=150)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')


class UserAddress(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_addresses')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='users_addresses')
