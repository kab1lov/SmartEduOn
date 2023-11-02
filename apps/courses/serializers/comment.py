from rest_framework.serializers import ModelSerializer

from apps.courses.models.comment import Comment


class CommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'course')


