from django.contrib import admin

from apps.courses.models.comment import Comment
from apps.courses.models.course import Category, Course
from apps.courses.models.module import Module
from apps.courses.models.teach_stage import Stage
from apps.courses.models.video import Video, File, Test, Certification

# class CourseAdminForm(forms.ModelForm):
#     description = forms.CharField(widget=CKEditorWidget())
#
#     class Meta:
#         model = Course
#         fields = '__all__'
#
#
# class CourseAdmin(admin.ModelAdmin):
#     form = CourseAdminForm
#
#
# admin.site.register(Course, CourseAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Course)
# admin.site.register(Speaker)
admin.site.register(Video)
admin.site.register(File)
admin.site.register(Test)
admin.site.register(Certification)
admin.site.register(Module)
admin.site.register(Stage)
