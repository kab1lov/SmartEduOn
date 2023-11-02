from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from apps.courses.models.course import Course
from apps.courses.models.teach_stage import Stage
from apps.courses.permission import IsAdminOrReadOnly
from apps.courses.serializers.course import CourseModelSerializer
from apps.courses.serializers.teach_stage import StageModelSerializer


class StageListCreateAPIView(ListCreateAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageModelSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)


class CourseSearchListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
