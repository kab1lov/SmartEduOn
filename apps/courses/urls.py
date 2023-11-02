from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.courses.views.comment import CommentListCreateAPIView
from apps.courses.views.course import (CourseDetailRetrieveAPIView, TopCoursesAPIView, FilterListAPIView,
                                       CategoryListCreateAPIView, NewCoursesListAPIView, CourseDetailViewSet,
                                       AddFreeCourseToMyCoursesView)
from apps.courses.views.course import CourseModelViewSet
from apps.courses.views.course import SpeakerCourseListAPIView
from apps.courses.views.course import UserPaymeListView
from apps.courses.views.rank import RatingCreateView
from apps.courses.views.speaker import (SpeakerTopListAPIView, SpeakerInformationListAPIView, SpeakerProfileListAPIView,
                                        SpeakerProfileDetailAPIView)
from apps.courses.views.teach_stage import StageListCreateAPIView, CourseSearchListAPIView
from apps.courses.views.video import (VideoListCreateAPIView, VideoListUpdateDestroyAPIView)

router = DefaultRouter()

# router.register('speaker_profile', SpeakerModelViewSet, 'speaker_profile')

urlpatterns = [
    # path('', include(router.urls)),
    path('course_search', CourseSearchListAPIView.as_view()),
    path('course_create', CourseModelViewSet.as_view()),
    path('course/<int:pk>/', CourseDetailViewSet.as_view()),

    path('speaker_course_list/<int:user_id>', SpeakerCourseListAPIView.as_view()),
    path('speaker_info', SpeakerInformationListAPIView.as_view()),
    # path('speaker_profile', SpeakerProfileListAPIView.as_view()),
    path('speaker-profile/<int:user_id>/', SpeakerProfileDetailAPIView.as_view()),
    path('speaker_top', SpeakerTopListAPIView.as_view()),
    path('ratings_speaker', RatingCreateView.as_view()),
    # path('ratings_course', RatingCourseCreateView.as_view()),
    # path('speaker_card', SpeakerCardListAPIView.as_view()),

    path('speaker_video_upload', VideoListCreateAPIView.as_view()),
    path('speaker_video/<int:pk>/', VideoListUpdateDestroyAPIView.as_view()),
    # path('speaker_test_upload', TestListCreateAPIView.as_view()),
    # path('speaker_file_upload', FileListCreateAPIView.as_view()),
    # path('speaker_certification_upload', CertificationListCreateAPIView.as_view()),

    path('category', CategoryListCreateAPIView.as_view()),
    path('comment', CommentListCreateAPIView.as_view()),
    # path('module/<int:pk>', ModuleListCreateAPIView.as_view()),

    path('course_detail/<int:pk>', CourseDetailRetrieveAPIView.as_view()),
    path('course_new', NewCoursesListAPIView.as_view()),
    path('course_top', TopCoursesAPIView.as_view()),

    path('filter', FilterListAPIView.as_view()),
    # path('teach_stage', StageListCreateAPIView.as_view()),

    path('users/payments', UserPaymeListView.as_view(), name='user-payments'),
    path('add_free_course', AddFreeCourseToMyCoursesView.as_view()),

]
