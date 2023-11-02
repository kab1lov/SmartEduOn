from ckeditor.fields import RichTextField
from django.db.models import CharField, FileField, ForeignKey, CASCADE

from shared.drf.models import BaseModel


class Video(BaseModel):
    title = CharField(max_length=255)
    description = RichTextField()
    duration = CharField(max_length=15, blank=True, null=True)
    video = FileField(upload_to='videos/video/', blank=True, null=True)

    author = ForeignKey('users.User', CASCADE, blank=True, null=True)
    course = ForeignKey('courses.Course', CASCADE)
    module = ForeignKey('courses.Module', CASCADE, blank=True, null=True)
    file = ForeignKey('courses.File', CASCADE, blank=True, null=True)


    def __str__(self):
        return self.title


class File(BaseModel):
    title = CharField(max_length=255)
    file = FileField(upload_to='files/file/', blank=True, null=True)

    author = ForeignKey('users.User', CASCADE)

    def __str__(self):
        return self.title


class Test(BaseModel):
    title = CharField(max_length=255)
    file = FileField(upload_to='tests/test/', blank=True, null=True)

    author = ForeignKey('users.User', CASCADE)

    def __str__(self):
        return self.title


class Certification(BaseModel):
    title = CharField(max_length=255)
    file = FileField(upload_to='certifications/certification/', blank=True, null=True)

    author = ForeignKey('users.User', CASCADE)

    def __str__(self):
        return self.title
