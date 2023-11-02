from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from apps.courses.models.rank import Rating, RatingCourse
from apps.courses.serializers.rank import RatingSerializer, RatingCourseSerializer


class RatingCreateView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    parser_classes = [MultiPartParser, FormParser]


class RatingCourseCreateView(CreateAPIView):
    queryset = RatingCourse.objects.all()
    serializer_class = RatingCourseSerializer
    parser_classes = [MultiPartParser, FormParser]
