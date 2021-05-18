from rest_framework import serializers
from rest_framework.response import Response

from mipha.apps.user.views import BaseAPIView
from mipha.models import BlogPost


class SearchWordsSerializer(serializers.Serializer):
    search_words = serializers.CharField(max_length=50)


class BlogSearchAPIView(BaseAPIView):
    """
    补全文本, 依照Fuzzy Search 对全文进行搜索
    limit 10
    """

    serializer_class = SearchWordsSerializer

    def get(self, request):
        return self.post(request)

    def post(self, request):
        serializer = SearchWordsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": 500, "error": "invalid params"})
        search_words = serializer.data["search_words"]
        suggestions = BlogPost.suggest_search(search_words)
        searched_posts = BlogPost.search_posts(search_words)

        return Response(
            {
                "status": "200",
                "results": {
                    "suggestions": suggestions,
                    "searched_posts": searched_posts,
                },
            }
        )


class BlogRecommendAPIView(BaseAPIView):
    """
    在某篇文章下面进行推荐
    limit 10
    推荐规则:
    1. 依照是否为同一个Guide [后期]
    2. 关键词与类型是否相近
    3. 点击率
    """

    def get(self, request):
        return Response("")


class SiteSearchAPIView(BaseAPIView):
    """
    依照关键词, 给出
    1. 同类关键词, limit 10
    2. 全文搜索的文章, limit 10
    """

    def get(self, request):
        return Response("")
