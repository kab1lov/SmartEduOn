from ckeditor.fields import RichTextField
from django.db.models import FileField

from shared.drf.models import BaseModel


class Stage(BaseModel):
    title = RichTextField()
    description = RichTextField()

    video = FileField(upload_to='stage/video', null=True, blank=True)

    def __str__(self):
        return self.title
