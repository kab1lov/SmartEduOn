from rest_framework.serializers import ModelSerializer

from apps.courses.models.module import Module


class ModuleModelSerializer(ModelSerializer):
    class Meta:
        model = Module
        exclude = ('created_at', 'updated_at')
