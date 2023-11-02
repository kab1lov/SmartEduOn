from django.http import Http404
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from apps.courses.models.speaker import Speaker
from apps.courses.pagination import CustomPagination
from apps.courses.serializers.speaker import (SpeakerProfileModelSerializer, SpeakerCardModelSerializer,
                                              SpeakerInformationModelSerializer, SpeakerCountSerializer, SpeakerProfile)
from apps.courses.views.video import VideoListCreateAPIView
from apps.users.models import User


class SpeakerModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SpeakerProfileModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)

    def speaker_profile(self):
        try:
            speaker = Speaker.objects.get(id=self.request.user.id)
        except Speaker.DoesNotExist:
            raise Http404("Speaker does not exist")


class SpeakerCardListAPIView(ListAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerCardModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def get_queryset(self):
        queryset = Speaker.objects.filter(speaker=self.request.user.id)
        if queryset is not None:
            return queryset
        else:
            return Speaker.objects.none()


class SpeakerInformationListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = SpeakerInformationModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        else:
            return User.objects.none()


class SpeakerTopListAPIView(ListAPIView):
    queryset = User.objects.filter(rating__gte=5).order_by('-rating')[:10]
    serializer_class = SpeakerCountSerializer
    permission_classes = [AllowAny]


class SpeakerProfileListAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = SpeakerProfile
    permission_classes = [AllowAny]
    parser_classes = [FormParser, MultiPartParser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        else:
            return User.objects.none()


class SpeakerProfileDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = SpeakerProfile
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return self.queryset.get(id=user_id)
