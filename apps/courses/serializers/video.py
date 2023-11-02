from rest_framework.serializers import ModelSerializer

from apps.courses.models.video import Video, Test, Certification, File


class VideoModelSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ('video', 'title', 'description', 'course')


class VideoCourseModelSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ('video', 'title', 'description')


class FileModelSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ('title', 'file')


class TestModelSerializer(ModelSerializer):
    class Meta:
        model = Test
        fields = ('title', 'file')


class CertificationModelSerializer(ModelSerializer):
    class Meta:
        model = Certification
        fields = ('title', 'file')
