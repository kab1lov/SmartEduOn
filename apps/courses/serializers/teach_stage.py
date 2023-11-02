from rest_framework.serializers import ModelSerializer

from apps.courses.models.teach_stage import Stage


class StageModelSerializer(ModelSerializer):
    class Meta:
        model = Stage
        exclude = ('created_at', 'updated_at')



