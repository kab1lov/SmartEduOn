from rest_framework import status
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.courses.models.video import Video, Test, Certification, File
from apps.courses.serializers.video import (VideoModelSerializer, FileModelSerializer, TestModelSerializer,
                                            CertificationModelSerializer)


class VideoListCreateAPIView(ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            success_message = "Video added successfully"
            return Response({"message": success_message}, status=status.HTTP_201_CREATED)
        else:
            error_message = "Invalid data provided"
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoListUpdateDestroyAPIView(RetrieveAPIView,UpdateAPIView, DestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        success_message = "Your video was successfully updated"
        return Response({"message": success_message}, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        success_message = "Your video was successfully deleted"
        instance.delete()
        return Response({"message": success_message}, status=status.HTTP_200_OK)


class FileListCreateAPIView(ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        success_message = "Fileingiz muvaffaqiyatli qo'shildi"
        return Response({"message": success_message}, status=status.HTTP_201_CREATED)


class TestListCreateAPIView(ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        success_message = "Testingiz muvaffaqiyatli qo'shildi"
        return Response({"message": success_message}, status=status.HTTP_201_CREATED)


class CertificationListCreateAPIView(ListCreateAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        success_message = "Sertificatingiz muvaffaqiyatli qo'shildi"
        return Response({"message": success_message}, status=status.HTTP_201_CREATED)
