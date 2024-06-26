# Generated by Django 3.2.3 on 2021-05-18 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        max_length=100,
                        unique=True,
                        verbose_name="分类名",
                    ),
                ),
                (
                    "order_num",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="排序"
                    ),
                ),
            ],
            options={
                "verbose_name": "博客分类",
                "verbose_name_plural": "博客分类",
                "db_table": "blog_category",
            },
        ),
        migrations.CreateModel(
            name="BlogTag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        max_length=100,
                        unique=True,
                        verbose_name="标签名",
                    ),
                ),
                (
                    "order_num",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="排序"
                    ),
                ),
            ],
            options={
                "verbose_name": "博客标签",
                "verbose_name_plural": "博客标签",
                "db_table": "blog_tag",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "username",
                    models.CharField(max_length=50, unique=True, verbose_name="用户名"),
                ),
                (
                    "mobile",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=20,
                        unique=True,
                        verbose_name="手机",
                    ),
                ),
                (
                    "avatar",
                    models.URLField(
                        blank=True, max_length=255, verbose_name="头像链接"
                    ),
                ),
            ],
            options={
                "verbose_name": "用户账号",
                "verbose_name_plural": "用户账号",
                "db_table": "user",
            },
        ),
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, unique=True, verbose_name="标题"),
                ),
                ("content", models.TextField(verbose_name="内容")),
                ("char_num", models.IntegerField(default=0, verbose_name="字数统计")),
                (
                    "allow_comments",
                    models.BooleanField(default=True, verbose_name="允许评论"),
                ),
                ("vote_num", models.IntegerField(default=0, verbose_name="点赞数量")),
                (
                    "publish_date",
                    models.DateTimeField(
                        blank=True, db_index=True, null=True, verbose_name="发表时间"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="category_posts",
                        to="playbase.blogcategory",
                        verbose_name="博文种类",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        related_name="tags_posts",
                        to="playbase.BlogTag",
                        verbose_name="标签",
                    ),
                ),
            ],
            options={
                "verbose_name": "博客博文",
                "verbose_name_plural": "博客博文",
                "db_table": "blog_post",
            },
        ),
    ]
