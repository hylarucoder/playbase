from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from mipha.models import BlogCategory, BlogTag, BlogPost
from .base import BaseAPIView
from ..pagenations import SmallResultsSetPagination


class BlogCategoryCountSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = BlogCategory
        fields = "__all__"


class BlogTagCountSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = BlogTag
        fields = "__all__"


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = "__all__"


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = "__all__"


class BlogPostSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            "id",
            "title",
            "char_num",
            "content",
            "vote_num",
            "category",
            "tags",
            "publish_date",
        )


class BlogPostListSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    title = serializers.CharField()
    id = serializers.IntegerField()

    class Meta:
        model = BlogPost
        fields = (
            "id",
            "title",
            "char_num",
            "vote_num",
            "category",
            "tags",
            "publish_date",
        )


class BlogPostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="contains")
    having_tags = filters.Filter(name="tags", lookup_expr="in")

    class Meta:
        model = BlogPost
        fields = ("title", "char_num", "category", "tags")


class BlogCategoryAPIView(BaseAPIView):
    def get(self, request):
        bc = (
            BlogCategory.objects.annotate(count=Count("category_posts"))
            .order_by("-count")
            .all()
        )
        serializer = BlogCategoryCountSerializer(bc, many=True)
        res = {"results": serializer.data}
        return Response(res)


class BlogTagsAPIView(BaseAPIView):
    def get(self, request):
        bt = (
            BlogTag.objects.annotate(count=Count("tags_posts")).order_by("-count").all()
        )
        serializer = BlogTagCountSerializer(bt, many=True)
        res = {"results": serializer.data}
        return Response(res)


class BlogPostListAPIView(generics.ListAPIView):
    """
    依照 category , tags , 时间 (年/月/日  年/月 年)
    """

    queryset = BlogPost.objects.all()
    serializer_class = BlogPostListSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filter_class = BlogPostFilter
    ordering_fields = ("publish_date",)
    ordering = ("publish_date",)
    permission_classes = (permissions.AllowAny,)
    pagination_class = SmallResultsSetPagination


class BlogPostAPIView(BaseAPIView):
    """
    获取单个
    """

    def get(self, request, title):
        bp = BlogPost.objects.get(title=title)
        serializer = BlogPostSerializer(bp)
        return Response(serializer.data)


class BlogPostArchiveAPIView(BaseAPIView):
    """
    获取列表
    """

    def get(self, request):
        bps = (
            BlogPost.objects.only("title", "publish_date", "char_num", "vote_num")
            .all()
            .order_by("-publish_date")
        )
        timelines = []
        months = sorted(
            list(set(map(lambda x: x.publish_date.strftime("%Y-%m"), bps))),
            reverse=True,
        )
        for month in months:
            timelines.append({"month": month, "articles": []})
        for bp in bps:
            m = bp.publish_date.strftime("%Y-%m")
            tl = list(filter(lambda x: x["month"] == m, timelines))[0]
            tl["articles"].append(
                {
                    "title": bp.title,
                    "publish_date": bp.publish_date,
                    "char_num": bp.char_num,
                    "vote_num": bp.vote_num,
                }
            )
        return Response({"results": timelines})
