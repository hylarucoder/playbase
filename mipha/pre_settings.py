import os
import pathlib
from functools import lru_cache

import django
from pydantic import BaseSettings

ROOT_PATH = str(pathlib.Path(__file__).parent.absolute())


class Settings(BaseSettings):
    DEBUG: bool = False
    SECRET_KEY: str = "changethisbeforedeployproduction"
    TIME_ZONE: str = "Asia/Shanghai"
    REDIS_URI: str = "redis://redis/0"
    ROOT_PATH: str = ROOT_PATH


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def pre_setting():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mipha.settings")
    django.setup()
