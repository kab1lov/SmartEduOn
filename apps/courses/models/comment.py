from django.db.models import CharField, ForeignKey, CASCADE

from shared.drf.models import BaseModel


class Comment(BaseModel):
    text = CharField(max_length=255)

    course = ForeignKey('courses.Course', CASCADE, related_name='course', null=True, blank=True)
    author = ForeignKey('users.User', CASCADE, related_name='author')

    class Meta:
        ordering = ('-created_at',)



