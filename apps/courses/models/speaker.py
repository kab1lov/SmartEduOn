from ckeditor.fields import RichTextField
from django.db.models import (CharField, ImageField, IntegerField, DateField, CASCADE, FileField, OneToOneField)

from shared.drf.models import BaseModel


class Speaker(BaseModel):
    speaker = OneToOneField('users.User', CASCADE, related_name='speaker_profile')
    phone = CharField(max_length=20, null=True, blank=True)
    information = RichTextField()
    job = CharField(max_length=250, null=True)
    company = CharField(max_length=250, null=True)
    birth_date = DateField(null=True, blank=True)
    country = CharField(max_length=50, null=True, blank=True)
    city = CharField(max_length=50, null=True, blank=True)

    logo = ImageField(upload_to='speakers/logo/image', null=True, blank=True)
    image = ImageField(upload_to='speakers/images', null=True, blank=True)
    video_info = FileField(upload_to='speakers/video', null=True, blank=True)
    view = IntegerField(default=0)

    # rating = ForeignKey(Rank, CASCADE, related_name='speaker_rank', null=True, blank=True)

    card_number = CharField(max_length=50, null=True, blank=True)
    card_name = CharField(max_length=50, null=True, blank=True)
    card_expire = CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.speaker.username

    def get_speaker(self):
        return self.speaker
