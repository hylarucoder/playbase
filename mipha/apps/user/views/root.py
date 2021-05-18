from rest_framework.response import Response

from .base import BaseAPIView


class APIRootView(BaseAPIView):
    """
    以**动手实践**为荣，以**只看不练**为耻。

    以**打印日志**为荣，以**出错不报**为耻。

    以**局部变量**为荣，以**全局变量**为耻。

    以**单元测试**为荣，以**手工测试**为耻。

    以**代码重用**为荣，以**复制粘贴**为耻。

    以**多态应用**为荣，以**分支判断**为耻。

    以**定义常量**为荣，以**魔法数字**为耻。

    以**总结思考**为荣，以**不求甚解**为耻。
    """

    def get(self, request, format=None):
        HTTP_HOST = request.META["HTTP_HOST"]
        data = [
            {
                "公用模块": {
                    "获取应用信息": "api/system/info",
                },
                "登录模块": {
                    "获取认证Token": "api/account/api-token-auth",
                    "刷新登录Token": "api/account/api-token-refresh",
                    "验证登录Token": "api/account/api-token-verify",
                },
                "博客模块": {
                    "获取简历信息": "api/blog/resume",
                },
            },
        ]
        for index, item in enumerate(data):
            for k, v in item.items():
                for t_k, t_v in v.items():
                    value = t_v
                    new_value = "http://" + HTTP_HOST + "/" + value
                    data[index][k][t_k] = new_value
        return Response(data)
