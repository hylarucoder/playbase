import pprint

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.conf import settings
import os
from django.utils import timezone

from django_celery_results.models import TaskResult
from django_celery_beat.models import SolarSchedule, IntervalSchedule, CrontabSchedule, PeriodicTasks, PeriodicTask


class Command(BaseCommand):
    """
    """

    def handle(self, *args, **options):
        models = [SolarSchedule, IntervalSchedule, CrontabSchedule, PeriodicTasks, PeriodicTask]
        for m in models:
            m.objects.all().delete()
