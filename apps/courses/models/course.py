from ckeditor.fields import RichTextField
from django.db.models import (CharField, SET_NULL, TextChoices, ForeignKey, ImageField, IntegerField,
                              CASCADE, DecimalField)
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from shared.drf.models import BaseModel


class Category(MPTTModel):
    name = CharField(max_length=155)
    parent = TreeForeignKey('self', SET_NULL, 'subcategory', blank=True, null=True)

    def __str__(self):
        return self.name


class Course(BaseModel):
    class LanguageChoice(TextChoices):
        EN = 'en'
        RU = 'ru'
        UZ = 'uz'

    class DegreeChoice(TextChoices):
        PRIMARY = 'primary'
        MEDIUM = 'medium'
        HIGH = 'high'

    class TypeChoice(TextChoices):
        PAID = 'paid'
        FREE = 'free'

    name = CharField(max_length=255)
    description = RichTextField()
    key_word = CharField(max_length=255, null=True, blank=True)
    whos_course = CharField(max_length=255)
    price = IntegerField(default=0)
    image = ImageField(upload_to='courses/')
    view = IntegerField(default=0)
    discount = IntegerField(default=0)

    language = CharField(max_length=5, choices=LanguageChoice.choices, default=LanguageChoice.UZ)
    type = CharField(max_length=10, choices=TypeChoice.choices, default=TypeChoice.FREE)
    degree = CharField(max_length=10, choices=DegreeChoice.choices, default=DegreeChoice.PRIMARY)
    rating = DecimalField(max_digits=2, decimal_places=2, default=0.0)

    speaker = ForeignKey('users.User', SET_NULL, null=True, blank=True, related_name='course')
    category = ForeignKey('courses.Category', SET_NULL, null=True, blank=True)

    # @property
    # def comments_count(self):
    #     return self.comment_set.count()

    @property
    def discount_price(self):
        return self.price - self.price * self.discount // 100

    def get_video(self):
        return self.video_set.all()

    def get_comments(self):
        return self.course.all()

    def get_course(self):
        return self.course.all()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class ViewedProduct(BaseModel):
    user = ForeignKey('users.User', CASCADE)
    course = ForeignKey('courses.Course', CASCADE)

    def __str__(self):
        return self.user


class UserCourse(BaseModel):
    user = ForeignKey('users.User', on_delete=CASCADE)
    course = ForeignKey('courses.Course', on_delete=CASCADE)
