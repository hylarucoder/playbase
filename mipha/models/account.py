from django.db import models

from mipha.models.base import Model


class User(Model):
    class Meta:
        verbose_name = verbose_name_plural = "用户账号"
        db_table = 'user'

    id = models.BigAutoField(primary_key=True)
    username = models.CharField(
        "用户名",
        max_length=50,
        unique=True,
    )
    mobile = models.CharField(
        max_length=20,
        blank=True,
        db_index=True,
        unique=True,
        verbose_name="手机",
    )
    avatar = models.URLField(max_length=255, blank=True, verbose_name="头像链接")

    def __str__(self):
        return "<Account # %d, %s>" % (self.id, self.username)
