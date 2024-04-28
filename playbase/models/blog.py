from django.db import models

from playbase.models import Model


class BlogCategory(Model):
    class Meta:
        verbose_name = verbose_name_plural = "博客分类"
        db_table = "blog_category"

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        verbose_name="分类名",
        db_index=True,
        unique=True,
        null=False,
        blank=False,
        max_length=100,
    )
    order_num = models.IntegerField(
        verbose_name="排序", default=0, blank=True, null=True
    )

    def __str__(self):
        return self.name


class BlogTag(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "博客标签"
        db_table = "blog_tag"

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        verbose_name="标签名",
        db_index=True,
        unique=True,
        null=False,
        blank=False,
        max_length=100,
    )
    order_num = models.IntegerField(
        verbose_name="排序", default=0, blank=True, null=True
    )

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "博客博文"
        db_table = "blog_post"

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name="标题", unique=True, max_length=255)
    content = models.TextField(verbose_name="内容")
    char_num = models.IntegerField(verbose_name="字数统计", default=0)

    allow_comments = models.BooleanField(verbose_name="允许评论", default=True)
    vote_num = models.IntegerField(verbose_name="点赞数量", default=0)
    category = models.ForeignKey(
        BlogCategory,
        verbose_name="博文种类",
        related_name="category_posts",
        null=True,
        on_delete=models.SET_NULL,
    )
    tags = models.ManyToManyField(
        BlogTag, verbose_name="标签", related_name="tags_posts"
    )

    publish_date = models.DateTimeField(
        "发表时间", blank=True, null=True, db_index=True
    )

    def __str__(self):
        return "{} - {} - {}".format(self.pk, self.title, self.publish_date)


class Message(models.Model):
    class Meta:
        db_table = "message"

    id = models.BigAutoField(primary_key=True)
    user_message = models.TextField()
    bot_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MockTask(models.Model):
    class Meta:
        db_table = "mock_task"

    id = models.BigAutoField(primary_key=True)
    category = models.CharField(max_length=50, db_index=True)
    description = models.TextField()
    status = models.CharField(max_length=50, db_index=True)
    priority = models.CharField(max_length=50, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
