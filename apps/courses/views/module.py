from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.courses.models.module import Module
from apps.courses.serializers.module import ModuleModelSerializer


class ModuleListCreateAPIView(ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)


