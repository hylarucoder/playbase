import os
import pprint
from collections import Counter

import yaml
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

STATUS_NEED_ADD = 1
STATUS_NEED_UPDATE = 2
STATUS_NEED_DELETE = 3


class Command(BaseCommand):
    """
    每次导入数据的时候,
    1. 要保持 Markdown 文件和 BlogPost 文件数量保持一致
    2. 清理无用文件
    """

    help = "导入根目录下hexo-post里面的文章"

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super().__init__(stdout, stderr, no_color)
        self.categories_counter = Counter()
        self.tags_counter = Counter()

    def handle(self, *args, **options):
        hexo_path = settings.ROOT_PATH + "/hexo-posts"
        files = sorted(
            list(
                filter(
                    lambda x: x.endswith(".md"),
                    map(lambda x: hexo_path + "/" + x, os.listdir(hexo_path)),
                )
            )
        )
        exist_blogposts = list(BlogPost.objects.all())
        exist_titles = set([blogpost.title for blogpost in exist_blogposts])

        file_status_list = []
        # TODO : 判断标题是否唯一
        # 默认都是需要添加 , 判断需要 更新 的文章
        # 剩下来的只有需要删除的.新增的
        for file in files:
            with open(file, "rt") as f:
                file_content = f.read()
                header, content = file_content.split("---", 1)
                article_info = yaml.load(header)
                file_status = {
                    "file": file,
                    "status": STATUS_NEED_ADD,
                    "title": article_info["title"],
                }
                if file_status["title"] in exist_titles:
                    """需要增加"""
                    file_status["status"] = STATUS_NEED_UPDATE
                    exist_titles.remove(file_status["title"])
                else:
                    file_status["status"] = STATUS_NEED_ADD
                file_status_list.append(file_status)

        # 从需要删除与新增的里面判断出需要删除的,剩下的为需要新增的数量

        need_delete_titles = exist_titles

        need_update_titles = set(
            map(
                lambda x: x["title"],
                filter(lambda x: x["status"] == STATUS_NEED_UPDATE, file_status_list),
            )
        )

        need_add_titles = set(
            map(
                lambda x: x["title"],
                filter(lambda x: x["status"] == STATUS_NEED_ADD, file_status_list),
            )
        )

        print("S1 正在删除无用文章...")
        # BlogPost.objects.filter(Q(title__in=need_delete_titles)).delete()
        for idx, blogpost in enumerate(exist_blogposts):
            if blogpost.title in need_delete_titles:
                blogpost.delete()

        print("S2 正在更新文章...")
        for idx, blogpost in enumerate(exist_blogposts):
            if blogpost.title in need_update_titles:
                file_status = list(
                    filter(lambda x: x["title"] == blogpost.title, file_status_list)
                )
                if file_status:
                    file_status = file_status[0]
                file = file_status["file"]
                self.process_blogpost(file)

        print("S3 正在新增文章...")
        for idx, title in enumerate(need_add_titles):
            file_status = list(filter(lambda x: x["title"] == title, file_status_list))
            if file_status:
                file_status = file_status[0]
            file = file_status["file"]
            self.process_blogpost(file)

        print("S4 正在清理无用的分类...")
        for idx, blogcategory in enumerate(BlogCategory.objects.all()):
            if blogcategory.category_posts.count() == 0:
                blogcategory.delete()

        print("S5 正在清理无用的标签...")
        for idx, blogtag in enumerate(BlogTag.objects.all()):
            if blogtag.tags_posts.count() == 0:
                blogtag.delete()

        BlogPost.bulk_indexing()

        pprint.pprint(
            {
                "添加文章": len(need_add_titles),
                "删除文章": len(need_delete_titles),
                "更新文章": len(need_update_titles),
            }
        )

        self.init_user()

    def init_user(self):
        c = Account.objects.all().count()
        if c == 0:
            u = Account()
            u.username = "admin"
            u.email = "admin"
            u.telephone = "18117454353"
            u.set_password("admin123123")
            u.is_staff = True
            u.is_superuser = True
            u.save()

    def process_blogpost(self, file):
        with open(file, "rt") as f:
            file_content = f.read()
            # print(file_content)
            header, content = file_content.split("---", 1)
            article_info = yaml.load(header)
            article_info["content"] = content
            self.categories_counter.update({article_info["categories"][0]: 1})
            for tags_dict in list(map(lambda x: {x: 1}, article_info["tags"])):
                self.tags_counter.update(tags_dict)
            article_info["created"] = article_info["date"]
            article_info["updated"] = article_info["date"]

            blogcategory, created = BlogCategory.objects.get_or_create(
                name=article_info["categories"][0]
            )
            if created:
                blogcategory.save()

            tags = []
            for tag_name in article_info["tags"]:
                blogtag, created = BlogTag.objects.get_or_create(name=tag_name)
                if created:
                    blogcategory.save()
                tags.append(blogtag)
                pass

            try:
                blogpost = BlogPost.objects.filter(Q(title=article_info["title"]))[0]
            except Exception as e:
                blogpost = BlogPost()
                blogpost.title = article_info["title"]
                pass

            blogpost.content = article_info["content"]
            blogpost.char_num = len(article_info["content"])
            blogpost.allow_comments = False
            blogpost.publish_date = timezone.make_aware(
                article_info["date"], timezone.get_current_timezone()
            )
            blogpost.category = blogcategory
            blogpost.save()
            if len(tags) > 0:
                blogpost.tags.set(tags)
            blogpost.save()
