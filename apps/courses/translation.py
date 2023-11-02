# from modeltranslation.translator import register, TranslationOptions
#
# from apps.courses.models.comment import Comment
# from apps.courses.models.course import Course, Category
# from apps.courses.models.module import Module
# from apps.courses.models.speaker import Speaker
# from apps.courses.models.comment import FeedBack
# from apps.courses.models.teach_stage import Stage
# from apps.courses.models.video import Video
# from apps.courses.models.video import File
# from apps.courses.models.video import Test
# from apps.courses.models.video import Certification
#
#
# @register(Course)
# class CourseTranslationOption(TranslationOptions):
#     fields = ('name', 'description', 'type', 'degree')
#
#
# @register(Category)
# class CourseTranslationOption(TranslationOptions):
#     fields = ('name',)
#
#
#
#
# @register(Module)
# class ModuleTranslationOption(TranslationOptions):
#     fields = ('title',)
#
#
# @register(Stage)
# class StageTranslationOption(TranslationOptions):
#     fields = ('title', 'description')
#
#
# @register(Video)
# class VideoTranslationOption(TranslationOptions):
#     fields = ('title', 'description')
#
#
# @register(File)
# class FileTranslationOption(TranslationOptions):
#     fields = ('title',)
#
#
# @register(Test)
# class TestTranslationOption(TranslationOptions):
#     fields = ('title',)
#
#
# @register(Certification)
# class TestTranslationOption(TranslationOptions):
#     fields = ('title',)
#
#
# @register(Speaker)
# class SpeakerTranslationOption(TranslationOptions):
#     fields = ('information', 'job', 'company', 'country', 'city')
