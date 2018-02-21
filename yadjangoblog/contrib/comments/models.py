"""
# inspired by https://github.com/r26zhao/django-easy-comment/
"""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.conf import settings
from mptt.models import TreeForeignKey, MPTTModel

from yacommon.models import Ownable


class Comment(Ownable, MPTTModel):
    commented_object = GenericForeignKey('content_type', 'object_id')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='父级评论')
    content = models.TextField(verbose_name='评论内容', blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        if self.parent is not None:
            return '{} 回复 {}'.format(self.owner.username, self.parent.owner.username)
        return '{} 评论 实体 {}'.format(self.owner.username, self.parent.owner.username)


VOTES_TYPE = (
    (-1, "踩"),
    (0, "无"),
    (1, "顶"),
)


class Vote(Ownable, models.Model):
    voted_object = GenericForeignKey('content_type', 'object_id')
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=True)

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.status:
            return '%s 赞了 %s的评论' % (self.owner.username, self.voted_object)
        return '%s 踩了 %s的评论' % (self.owner.username, self.voted_object)
