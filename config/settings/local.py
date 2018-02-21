# -*- coding: utf-8 -*-
"""
Local settings
- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""

import datetime
import urllib
from urllib import parse

from django.conf import settings

from .base import *

# DEBUG
# ------------------------------------------------------------------------------
if DEBUG:
    # django-debug-toolbar
    # ------------------------------------------------------------------------------
    # MIDDLEWARE += ['commons.middleware.XForwardedForMiddleware']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INSTALLED_APPS += ('debug_toolbar',)
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
        'JQUERY_URL': "//cdn.bootcss.com/jquery/2.2.4/jquery.min.js",
        # 'JQUERY_URL': "http://cdn.bootcss.com/jquery/2.1.1/jquery.min.js",
    }

    # django-extensions
    # ------------------------------------------------------------------------------
    INSTALLED_APPS += ('django_extensions',)
else:
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        )
    }
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'changethisbeforedeployproduction')

# CACHING
# ------------------------------------------------------------------------------
# TODO: 以后改到环境变量里面
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{host}:{port}/1"
            .format(host=os.getenv("REDIS_HOST", "redis"),
                    port=os.getenv("REDIS_PORT", "6379")),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "PASSWORD": os.getenv("REDIS_PASSWORD", "mysecret")
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ========== CELERY
CELERY_BROKER_URL = "redis://:{password}@{host}:{port}/1".format(
    password=parse.quote(os.getenv("REDIS_PASSWORD", "yourpass")),
    host=os.getenv("REDIS_HOST", "redis"),
    port=os.getenv("REDIS_PORT", "6379"),
)

# CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_RESULT_BACKEND = 'django-db'

CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_ALWAYS_EAGER = True
CELERY_IMPORTS = ("tasks")

CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# ========== END CELERY

# EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'sender@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'app_specific_password')
EMAIL_PORT = 587

# DOCKER TRICK
import socket
import os

# tricks to have debug toolbar when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + '1']

# TESTING
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DATABASE', 'yadjangoblog'),
        'USER': os.getenv('POSTGRES_USER', 'DJANGO'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'xxx123'),
        'HOST': os.getenv('POSTGRES_HOST', 'postgres'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'ATOMIC_REQUESTS': True,
    }
}

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': settings.SECRET_KEY,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

AUTH_USER_MODEL = 'yaaccounts.Account'

# Guardian的副作用, 直接去掉 AnonymousUser
ANONYMOUS_USER_NAME = None
