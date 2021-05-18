import os
import pathlib

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
ASSETS_DIR = "{}/static".format(str(ROOT_DIR))
APPS_DIR = os.path.join(str(ROOT_DIR), "mipha")

SECRET_KEY = "changethisbeforedeployproduction"

DEBUG = True

ALLOWED_HOSTS = ["*"]

DJANGO_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.contrib.admin",
)
THIRD_PARTY_APPS = (
    "rest_framework",
    "rest_framework_jwt",
    "guardian",
    "mptt",
    "django_filters"
)

LOCAL_APPS = (
    "mipha",
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ADMINS = (("""twocucao""", "twocucao@gmail.com"),)

MANAGERS = ADMINS

TIME_ZONE = "Asia/Shanghai"

USE_I18N = False
USE_L10N = True
USE_TZ = False

LANGUAGE_CODE = "zh-CN"
SITE_ID = 1

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(APPS_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_ROOT = os.getenv("STATIC_ROOT", os.path.join(ASSETS_DIR, "static"))
STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(APPS_DIR, "static"),)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MEDIA_ROOT = os.getenv("MEDIA_ROOT", os.path.join(ASSETS_DIR, "media"))
MEDIA_URL = "/media/"

ROOT_URLCONF = "mipha.urls"

WSGI_APPLICATION = "mipha.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

ADMIN_URL = "admin"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

GRAPPELLI_ADMIN_TITLE = "Micheal Gardner的编程小屋"

# GRAPPELLI_INDEX_DASHBOARD = "mipha.yaadmin.dashboard.CustomIndexDashboard"

CORS_ORIGIN_ALLOW_ALL = True

INTERNAL_IPS = [
    "127.0.0.1",
    "10.0.2.2",
]
