import os
import pathlib
import socket

from pydantic_settings import BaseSettings

APP_PATH = pathlib.Path(__file__).parent
ROOT_PATH = APP_PATH.parent.absolute()


class Settings(BaseSettings):
    DEBUG: bool = True
    SECRET_KEY: str = "changethisbeforedeployproduction"
    TIME_ZONE: str = "Asia/Shanghai"
    DATABASE_URL: str = (
        "postgresql://rocketbase:rocketbase%26123@postgres:5432/rocketbase"
    )
    REDIS_CACHE_URI: str = "redis://redis:6379/1"


settings = Settings()

SECRET_KEY = settings.SECRET_KEY

DEBUG = settings.DEBUG

ALLOWED_HOSTS = ["*"]

DJANGO_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.contrib.admin",
)

THIRD_PARTY_APPS = (
    "django_htmx",
    'django_components',
    'django_components.safer_staticfiles'
)

LOCAL_APPS = (
    "playbase",
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django_htmx.middleware.HtmxMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ADMINS = (("""twocucao""", "twocucao@gmail.com"),)

MANAGERS = ADMINS

TIME_ZONE = settings.TIME_ZONE

USE_I18N = False
USE_L10N = True
USE_TZ = False

LANGUAGE_CODE = "zh-CN"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # "DIRS": [
        #     os.path.join(APP_DIR, "templates"),
        #     # os.path.join(BASE_DIR, "templates"),
        # ],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                        "django_components.template_loader.Loader",
                    ],
                )
            ],
            "builtins": [
                "django_components.templatetags.component_tags",
            ],
        },
    },
]

STATIC_ROOT = ROOT_PATH / "static"
STATIC_URL = "/static/"

STATICFILES_DIRS = (
    APP_PATH / "static",
    ROOT_PATH / "components",
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MEDIA_ROOT = ROOT_PATH / "media"
MEDIA_URL = "/media/"

ROOT_URLCONF = "playbase.apps.urls"

WSGI_APPLICATION = "playbase.wsgi.application"

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
)

ADMIN_URL = "admin"

CORS_ORIGIN_ALLOW_ALL = True

INTERNAL_IPS = [
    "127.0.0.1",
    "10.0.2.2",
]

if DEBUG:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INSTALLED_APPS += ("debug_toolbar",)
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": [
            "debug_toolbar.panels.redirects.RedirectsPanel",
        ],
        "SHOW_TEMPLATE_CONTEXT": True,
    }

    INSTALLED_APPS += ("django_extensions",)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "LOCATION": settings.REDIS_CACHE_URI,
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# tricks to have debug toolbar when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "playbase",
        "USER": "playbase",
        "PASSWORD": "playbase123",
        "HOST": "postgres",
        "PORT": 5432,
    }
}

# Guardian的副作用, 直接去掉 AnonymousUser
ANONYMOUS_USER_NAME = None
