from pprint import pprint

from yablog.models4es import BlogPostIndex


def test_blogpost():
    # 问题1 搜索Django没有搜索出来????
    res = BlogPostIndex.search_posts("django")
    print(res)
    res = BlogPostIndex.suggest_word("数据")
    print(res)
