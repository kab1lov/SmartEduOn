from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import (RetrieveAPIView, ListAPIView, ListCreateAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.courses.filters import CourseFilter
from apps.courses.models.course import (Category, Course, UserCourse)
from apps.courses.models.course import ViewedProduct
from apps.courses.models.video import Video
from apps.courses.serializers.course import (CategoryModelSerializer, CourseModelSerializer,
                                             CourseDetailModelSerializer, CourseListModelSerializer,
                                             NewCourseModelSerializer, UserCourseSerializer)
from apps.courses.serializers.course import ViewedProductSerializer
from apps.payments.models import Payment
from apps.payments.serializers import PaymentModelSerializer


class FilterListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['max_price', 'category', 'language', 'degree']
    filterset_class = CourseFilter


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)


class CourseModelViewSet(ListCreateAPIView):
    serializer_class = CourseModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)

    def get_queryset(self):
        return Course.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(speaker=self.request.user)

        course_id = serializer.instance.id

        success_message = "Successfully added."

        response_data = {
            "message": success_message,
            "course_id": course_id
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class CourseDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailModelSerializer
    permission_classes = [AllowAny]

    # Similar products
    @action(detail=True, methods=['GET'])
    def similar_products(self, request, pk=None):
        product = self.get_object()
        similar_products = Course.objects.filter(category=product.category)[:5]
        serializer = CourseDetailModelSerializer(similar_products, many=True)
        return Response(serializer.data)

    # Products viewed
    @action(detail=True, methods=['POST'])
    def mark_viewed(self, request, pk=None):
        product = self.get_object()
        user = request.user
        viewed_product = ViewedProduct(user=user, product=product)
        viewed_product.save()
        serializer = ViewedProductSerializer(viewed_product)
        return Response(serializer.data)


class CourseDetailViewSet(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        course_id = instance.id

        video_ids = list(Video.objects.filter(course=instance).values_list('id', flat=True))

        response_data = {
            "course_id": course_id,
            "video_ids": video_ids
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(speaker=self.request.user)

        course_id = instance.id

        success_message = "Successfully updated."

        response_data = {
            "message": success_message,
            "course_id": course_id
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        success_message = "Successfully deleted."

        response_data = {
            "message": success_message
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class SpeakerCourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Course.objects.filter(speaker_id=user_id)


class SpeakerCourseModelViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)

    def get_queryset(self):
        queryset = Course.objects.filter(user_id=self.request.user.id)
        if queryset is not None:
            return queryset
        else:
            return Course.objects.none()


class TopCoursesAPIView(ListAPIView):
    queryset = Course.objects.order_by('-view')[:10]
    serializer_class = NewCourseModelSerializer
    permission_classes = [AllowAny]


class NewCoursesListAPIView(ListAPIView):
    queryset = Course.objects.get_queryset().order_by('-created_at')
    serializer_class = NewCourseModelSerializer
    permission_classes = [AllowAny]


class UserPaymeListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Payment.objects.filter(user_id=self.request.user.id)
        if queryset is not None:
            return queryset
        else:
            return Payment.objects.none()


class AddFreeCourseToMyCoursesView(ListCreateAPIView):
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        course_id = request.data.get('course', None)
        if course_id is None:
            return Response({"error": "Course ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        if course.type != Course.TypeChoice.FREE:
            return Response({"error": "This is not a free course."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        if UserCourse.objects.filter(user=user, course=course).exists():
            return Response({"message": "You already own this course."}, status=status.HTTP_200_OK)

        user_course = UserCourse(user=user, course=course)
        user_course.save()

        return Response({"message": "Course successfully added ."}, status=status.HTTP_201_CREATED)
