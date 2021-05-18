import os

from celery.schedules import crontab
from django.conf import settings
from django.core.cache import cache

from mipha.globals import celery
from mipha.models import User

if not settings.configured:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "mipha.settings"
    )  # pragma: no cover


def setup_celery():
    celery.conf.timezone = "Asian/Shanghai"
    celery.conf.broker_url = "redis://:{password}@redis:{port}/1"
    # celery.settings.beat = {}

    CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


setup_celery()


@celery.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))  # pragma: no cover


@celery.task
def test(arg):
    print(arg)


@celery.task
def test_beat(args):
    print("===> test beat", args)


@celery.task
def test_django_orm():
    print("===> test django orm")
    print(User.objects.first())


@celery.task
def test_redis():
    cache.incr("test_beat_exec")
    print("===> test_redis", cache.get("test_beat_exec"))


@celery.task
def test_elasticsearch():
    print("===> test_elasticsearch")


@celery.task
def test_django_orm():
    print(User.objects.first())


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=7, minute=30),
        test.s("Hceleryy Mondays!"),
    )
    sender.add_periodic_task(
        crontab(hour=6, minute=30, day_of_week=1),
        test.s("Hceleryy Mondays!"),
    )
