from rest_framework.serializers import ModelSerializer

from apps.courses.models.rank import Rating, RatingCourse


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'speaker', 'value')


class RatingCourseSerializer(ModelSerializer):
    class Meta:
        model = RatingCourse
        fields = ('id', 'course', 'value')
