from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import (
    DocType,
    Text,
    Date,
    Integer,
    Boolean,
    Completion,
    Search,
    Nested,
    InnerDoc,
    connections,
    Q,
)

from yablog.client4es import es_client

connections.create_connection(host="elasticsearch", port="9200")


class BlogPostIndex(DocType):
    id = Integer()
    title = Text(analyzer="ik_max_word", search_analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word", search_analyzer="ik_max_word")
    char_num = Integer()
    allow_comments = Boolean()
    vote_num = Integer()
    category = Text(analyzer="ik_max_word", search_analyzer="ik_max_word")
    tags = Text(analyzer="ik_max_word", search_analyzer="ik_max_word")
    publish_date = Date()
    suggestions = Completion()

    class Meta:
        index = "blogpost-index"

    @classmethod
    def add(cls, **kwargs):
        id = kwargs.pop("id", None)
        if id is None:
            return False
        blog = cls(meta={"id": id}, **kwargs)
        blog.save()
        return blog

    @staticmethod
    def search_posts(words, delim="......<br>......<br>......"):
        """
        用原生写法拼装结果
        :param words:
        :return:
        """
        q = {
            "_source": ["title", "category", "tags", "publish_date"],
            "query": {
                "bool": {
                    "must": [],
                    "must_not": [],
                    "should": [
                        {"term": {"tags": "{}".format(words)}},
                        {"term": {"title": "{}".format(words)}},
                        {"term": {"content": "{}".format(words)}},
                    ],
                }
            },
            "highlight": {
                "number_of_fragments": 3,
                "fragment_size": 150,
                "fields": {
                    "title": {"pre_tags": ["<em>"], "post_tags": ["</em>"]},
                    "content": {"pre_tags": ["<em>"], "post_tags": ["</em>"]},
                },
            },
            "from": 0,
            "size": 50,
            "sort": [],
            "aggs": {},
        }
        response = es_client.search(index="blogpost-index", body=q)
        r = []
        for item in response["hits"]["hits"]:
            if item.get("highlight", None):
                if item["highlight"].get("title", None):
                    title = "".join(item["highlight"]["title"])
                else:
                    title = item["_source"]["title"]
                if item["highlight"].get("content", None):
                    content = delim.join(item["highlight"]["content"]) + "......<br>"
                else:
                    content = ""
                r.append(
                    {
                        "origin_title": item["_source"]["title"],
                        "title": title,
                        "content": content,
                    }
                )
        return r

    @staticmethod
    def suggest_word(words):
        q = {
            "_source": False,
            "suggest": {
                "search-as-you-type-suggestion": {
                    "prefix": "{}".format(words),
                    "completion": {
                        "field": "suggestions",
                        "size": 10,
                        "fuzzy": {"fuzziness": 2},
                        "skip_duplicates": True,
                    },
                }
            },
        }
        response = es_client.search(index="blogpost-index", body=q)
        tmp = response["suggest"]["search-as-you-type-suggestion"]
        options = []
        if len(tmp) >= 1:
            options = [item["text"] for item in tmp[0]["options"]]
        return options

    @staticmethod
    def similar_recommends_post(words):
        pass
