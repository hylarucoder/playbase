from __future__ import annotations
from typing import Any, Optional

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise Http404()


class BaseManager(models.Manager):
    def get_or_404(self, pk):
        return get_object_or_404(super().get_queryset().filter(pk=pk))

    def first_or_404(self, **kwargs):
        return get_object_or_404(super().get_queryset().filter(**kwargs))


class Model(models.Model):
    id: Optional[int]

    class Meta:
        abstract = True

    objects = BaseManager()

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs)

    @classmethod
    def all(cls):
        return cls.objects.all()

    @classmethod
    def get(cls, pk):
        return cls.objects.get(pk=pk)

    @classmethod
    def get_or_404(cls, **kwargs) -> Model:
        return get_object_or_404(cls.objects.filter(**kwargs))

    @classmethod
    def find_or_404(cls, **kwargs) -> Model:
        return get_object_or_404(cls.objects.filter(**kwargs))

    @classmethod
    def find_first(cls, **kwargs) -> Model:
        return cls.objects.filter(**kwargs).first()

    @classmethod
    def one_or_404(cls, **kwargs) -> Model:
        return get_object_or_404(cls.objects.filter(**kwargs))

    @classmethod
    def first_or_404(cls, **kwargs) -> Model:
        return get_object_or_404(cls.objects.filter(**kwargs))

    def update_from_dict(self, obj: dict[str, Any], *fields: str):
        if not fields:
            for k, v in obj.items():
                setattr(self, k, v)
        else:
            for field in fields:
                setattr(self, field, obj[field])

    def partial_from_dict(self, obj: dict[str, Any], *fields: str):
        if not fields:
            for k, v in obj.items():
                setattr(self, k, v)
        else:
            for field in fields:
                setattr(self, field, obj[field])

    def incr(self, field):
        return self.__class__.objects.filter(id=self.id).update(**{field: F(field) + 1})

    def decr(self, field):
        return self.__class__.objects.filter(id=self.id).update(**{field: F(field) - 1})
