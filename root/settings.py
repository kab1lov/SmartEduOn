import os
from datetime import timedelta
from pathlib import Path

from ckeditor.fields import RichTextField
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ['*']

MY_APPS = [
    'apps.users',
    'apps.payments',
    'apps.courses',
    'apps.send_email',
    # 'apps.elastic_search',
]

THIRD_PARTY_APPS = [
    'mptt',
    'drf_yasg',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    # 'django_elasticsearch_dsl',
    # 'django_elasticsearch_dsl_drf',
]

INSTALLED_APPS = [
     'modeltranslation',
     'django.contrib.admin',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.messages',
     'django.contrib.staticfiles',

 ] + MY_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'root.wsgi.application'
ASGI_APPLICATION = 'root.asgi.application'

AUTH_USER_MODEL = 'users.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }
}

# Cache Config

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": "redis://redis:6379",
#     }
# }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
    ('uz', 'Uzbek'),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

# Static Config

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR / 'static')

# Media Config

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR / 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTH_USER_MODEL = 'auth.User'

# Email Config

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')

# Celery Configuration Options

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

CELERY_TIMEZONE = "Asia/Tashkent"

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# REST_FRAMEWORK Config

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 10,

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# JWT Config

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5, days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": os.getenv('SECRET_KEY'),
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ('Bearer',),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=10),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# Swagger Config

SWAGGER_SETTINGS = {
    'VALIDATOR_URL': 'http://localhost:8189',
    'DEFAULT_INFO': 'import.path.to.urls.api_info',
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Type in the *\'Value\'* input box below: **\'Bearer &lt;JWT&gt;\'**, '
                           'where JWT is the JSON web token you get back when logging in.'
        }
    }

}

# ElasticSearch Config
# ELASTICSEARCH_DSL = {
#     'default': {
#         'hosts': os.getenv('ELASTICSEARCH_URL')
#     },
# }

# CORS Config

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    # "http://207.154.247.30/",
]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with'
]

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_FILENAME_GENERATOR = 'apps.utils.get_filename'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'height': 300,
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', 'Indent', 'Outdent', 'Blockquote'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule'],
            ['Source'],
        ],
    },
}


#  PayMe

PAYCOM_SETTINGS = {
    'PAYCOM_ENV': True,
    'TOKEN': os.getenv('PAYME_TOKEN'),
    'SECRET_KEY': os.getenv('PAYME_SECRET_KEY'),
    'ACCOUNTS': {
        'KEY_1': 'order_id',
        'KEY_2': None
    }
}

CLICK_SERVICE_ID = os.getenv('CLICK_SERVICE_ID')
CLICK_MERCHANT_ID = os.getenv('CLICK_MERCHANT_ID')
CLICK_SECRET_KEY = os.getenv('CLICK_SECRET_KEY')
CLICK_MERCHANT_USER_ID = os.getenv('CLICK_MERCHANT_USER_ID')

# AWS S3

# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECedisET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_SIGNATURE_NAME = os.getenv('AWS_S3_SIGNATURE_NAME')
# AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
# AWS_S3_FILE_OVERWRITE = os.getenv('AWS_S3_FILE_OVERWRITE')
# AWS_DEFAULT_ACL = os.getenv('AWS_DEFAULT_ACL')
# AWS_S3_VERITY = os.getenv('AWS_S3_VERITY')
# DEFAULT_FILE_STORAGE = os.getenv('DEFAULT_FILE_STORAGE')

# Minio
# django-storages settings
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#
# DATA_UPLOAD_MAX_MEMORY_SIZE = 1048576000
# AWS_ACCESS_KEY_ID = os.getenv('MINIO_ACCESS_KEY')
# AWS_SECRET_ACCESS_KEY = os.getenv('MINIO_SECRET_KEY')
# AWS_STORAGE_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')
# AWS_S3_ENDPOINT_URL = os.getenv('MINIO_ENDPOINT')
#
# AWS_QUERYSTRING_AUTH = True
# AWS_QUERYSTRING_EXPIRE = 15



CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # Replace with your Redis server location
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}