from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from root import settings
from root.swagger import schema_view

urlpatterns = [

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('user/', include('apps.users.urls')),
    path('', include('apps.courses.urls')),
    path('', include('apps.send_email.urls')),
    # path('', include('apps.elastic_search.urls')),
    path('', include('apps.payments.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
