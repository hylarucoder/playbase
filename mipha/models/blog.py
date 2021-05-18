from django.db import models

from mipha.models import Model


class BlogCategory(Model):
    class Meta:
        verbose_name = verbose_name_plural = "博客分类"
        db_table = 'blog_category'

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        verbose_name="分类名",
        db_index=True,
        unique=True,
        null=False,
        blank=False,
        max_length=100,
    )
    order_num = models.IntegerField(verbose_name="排序", default=0, blank=True, null=True)

    def __str__(self):
        return self.name


class BlogTag(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "博客标签"
        db_table = 'blog_tag'

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        verbose_name="标签名",
        db_index=True,
        unique=True,
        null=False,
        blank=False,
        max_length=100,
    )
    order_num = models.IntegerField(verbose_name="排序", default=0, blank=True, null=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "博客博文"
        db_table = 'blog_post'

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
    tags = models.ManyToManyField(BlogTag, verbose_name="标签", related_name="tags_posts")

    publish_date = models.DateTimeField("发表时间", blank=True, null=True, db_index=True)

    def indexing(self):
        from yablog.models4es import BlogPostIndex

        obj = BlogPostIndex(
            meta={"id": self.id},
            title=self.title,
            content=self.content,
            char_num=self.char_num,
            allow_comments=self.allow_comments,
            vote_num=self.vote_num,
            category=self.category.name,
            tags=",".join([tag.name for tag in self.tags.all()]),
            suggestions={"input": [tag.name for tag in self.tags.all()]},
            publish_date=self.publish_date,
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    @classmethod
    def bulk_indexing(cls):
        BlogPostIndex.init()
        bulk(
            client=es_client,
            actions=(b.indexing() for b in cls.objects.all().iterator()),
        )

    @staticmethod
    def search_posts(words):
        """
        :return:
        """
        res = BlogPostIndex.search_posts(words)
        return res

    @staticmethod
    def suggest_search(word):
        """
        :return:
        """
        res = BlogPostIndex.suggest_word(word)
        return res

    def __repr__(self):
        return "{} - {} - {}".format(self.pk, self.title, self.publish_date)

    def __str__(self):
        return "{} - {} - {}".format(self.pk, self.title, self.publish_date)
