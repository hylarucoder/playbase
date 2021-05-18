from .base import *  # noqa

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "changethisbeforedeployproduction")

X_FRAME_OPTIONS = "DENY"

ALLOWED_HOSTS = ["*"]
