from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.courses.models.speaker import Speaker
from apps.courses.serializers.course import NewCourseModelSerializer
from apps.users.models import User


class SpeakerSerializer(ModelSerializer):
    class Meta:
        model = Speaker
        fields = ('phone', 'birth_date', 'job', 'country', 'city', 'logo', 'card_number', 'card_name', 'card_expire')


class SpeakerProfileModelSerializer(ModelSerializer):
    speaker = SerializerMethodField("get_speaker")

    def get_speaker(self, obj):
        speaker = Speaker.objects.filter(speaker=obj).values('phone', 'birth_date', 'job', 'country', 'city', 'logo',
                                                             'card_number', 'card_name', 'card_expire')

        for i in speaker:
            i["logo"] = "https://infonex.besenior.uz/media/" + i.get("logo")
        return speaker

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'speaker')


class SpeakerCardModelSerializer(ModelSerializer):
    class Meta:
        model = Speaker
        fields = ('card_number', 'card_name', 'card_expire')


class SpeakerInformationModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('image', 'about')


class SpeakersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ('id', 'speaker', 'job')

    # def to_representation(self, instance: Speaker):
    #     rep = super().to_representation(instance)
    #     rep['review_count'] = instance.rank_set.all().count()
    #     val = 0
    #     for i in instance.rank_set.all():
    #         val += i.value
    #     if val != 0:
    #         result = val / instance.rank_set.all().count()
    #         rep['rating'] = result
    #     return rep


class SpeakerCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'rating', 'image')


class SpeakerProfile(ModelSerializer):
    courses = SerializerMethodField("get_course")

    def get_course(self, obj):
        course = obj.course.all()
        serializer = NewCourseModelSerializer(course, many=True)
        for i in serializer.data:
            i["image"] = "https://infonex.besenior.uz" + i.get("image")
            # i["image"] = "http://127.0.0.1:8000" + i.get("image")
        return serializer.data

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'about', 'courses', 'username', 'job')
