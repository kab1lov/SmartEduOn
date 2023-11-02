from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.courses.models.course import Category, Course, UserCourse
from apps.courses.models.course import ViewedProduct
from apps.courses.serializers.comment import CommentModelSerializer
from apps.courses.serializers.video import VideoCourseModelSerializer


class NewCourseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name',  'view', 'image')


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['course_count'] = instance.course_set.count()
        return data


class CourseModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'id', 'name', 'description', 'image', 'whos_course',  'language',
            'type', 'degree', 'category')

    def create(self, validated_data):
        print(validated_data)
        user = validated_data['speaker']
        user.is_spiker = True
        user.save()
        return super().create(validated_data)


class ViewModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('view',)


class CourseListModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'image')


class CourseDetailModelSerializer(ModelSerializer):
    video = SerializerMethodField('get_video')
    comment = SerializerMethodField("get_comment")

    def get_video(self, obj):
        video = obj.video_set.all()
        serializer = VideoCourseModelSerializer(video, many=True, )
        for i in serializer.data:
            i["video"] = "https://infonex.besenior.uz" + i.get("video")
        return serializer.data

    def get_comment(self, obj):
        comment = obj.course.all()
        serializer = CommentModelSerializer(comment, many=True)
        return serializer.data

    class Meta:
        model = Course
        fields = ('name', 'description', 'speaker', 'image', 'whos_course',  'comment', 'video')


class ViewedProductSerializer(ModelSerializer):
    class Meta:
        model = ViewedProduct
        exclude = ()


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = ('course',)
