from django.db.models import CharField

from shared.drf.models import BaseModel


class Module(BaseModel):
    title = CharField(max_length=255)

    def __str__(self):
        return self.title
