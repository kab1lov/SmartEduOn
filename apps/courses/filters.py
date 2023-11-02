import django_filters
from django_filters import FilterSet, CharFilter

from apps.courses.models.course import Course


class CourseFilter(FilterSet):
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category__name = CharFilter(field_name='category__name', lookup_expr='icontains')
    language = CharFilter(field_name='language')
    degree = CharFilter(field_name='degree')

    class Meta:
        model = Course
        fields = ['category__name', 'max_price', 'language', 'degree']
