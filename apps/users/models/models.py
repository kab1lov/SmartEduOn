from django.db import models
from django.db.models import Model, CASCADE

from apps.courses.models.course import Course


class MyCourses(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='my_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='my_courses')


class Wishlist(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='wishlist')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='wishlist')


class Basket(Model):
    user = models.ForeignKey('users.User', on_delete=CASCADE, related_name='basket')
    course = models.ForeignKey(Course, on_delete=CASCADE, related_name='basket')
