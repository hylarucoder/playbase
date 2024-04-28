import os

import django


def pre_setting():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "playbase.settings")
    django.setup()
