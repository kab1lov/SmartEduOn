from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny

from apps.courses.models.comment import Comment
from apps.courses.serializers.comment import CommentModelSerializer


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer
    permission_classes = [AllowAny]
    parser_classes = (FormParser, MultiPartParser)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
