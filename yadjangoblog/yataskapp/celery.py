import os
from celery import Celery, shared_task
from celery.schedules import crontab
from django.apps import apps, AppConfig
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import caches, cache

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover

app = Celery('yadjangoblog')


class CeleryConfig(AppConfig):
    name = 'yadjangoblog.yataskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object('django.conf:settings', namespace='CELERY')
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # pragma: no cover


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@app.task
def test(arg):
    print(arg)


@app.task
def test_beat(args):
    print("===> test beat", args)


@app.task
def test_django_orm():
    print("===> test django orm")
    Account = get_user_model()
    print(Account.objects.first())


@app.task
def test_redis():
    cache.incr('test_beat_exec')
    print("===> test_redis", cache.get('test_beat_exec'))


@app.task
def test_elasticsearch():
    print("===> test_elasticsearch")


@app.task
def test_django_orm():
    Account = get_user_model()
    print(Account.objects.first())


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    cache.set('test_beat_exec', 1)
    # Calls test_beat every 10 seconds
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10 seconds')
    sender.add_periodic_task(10.0, test_redis.s(), name='add every 10 seconds')
    sender.add_periodic_task(10.0, test_elasticsearch.s(), name='add every 10 seconds')
    sender.add_periodic_task(10.0, test_django_orm.s(), name='add every 10 seconds')
    # Calls test_beat every 30 seconds
    sender.add_periodic_task(30.0, test.s('hello'), name='add every 30 seconds')
    # Calls test_beat every 60 seconds
    sender.add_periodic_task(60.0, test.s('hello'), name='add every 60 seconds')
    # Calls test_beat every 10 minutes
    sender.add_periodic_task(10 * 60.0, test.s('hello'), name='add every 10 minutes')
    # Calls test_beat every 30 minutes
    sender.add_periodic_task(30 * 60.0, test.s('hello'), name='add every 30 minutes')
    # Calls test_beat every 60 minutes
    sender.add_periodic_task(60 * 60.0, test.s('hello'), name='add every 60 minutes')
    # Calls test_beat every 12 hour
    sender.add_periodic_task(12 * 60 * 60.0, test.s('hello'), name='add every 12 hours')
    # Calls test_beat every 24 hour
    sender.add_periodic_task(24 * 60 * 60.0, test.s('hello'), name='add every 24 hours')

    # Executes every morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30),
        test.s('Happy Mondays!'),
    )
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=6, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


app.conf.timezone = 'UTC'
