from django.db import models


class Orderable(models.Model):
    order_num = models.IntegerField("排序", null=True)

    class Meta:
        abstract = True
