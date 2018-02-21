from rest_framework.response import Response

from yaapi.base.base_api_view import BaseAPIView
from yacommon.services.common import get_system_info, get_resume_info


class SystemInfo(BaseAPIView):
    """
    返回 web 应用的相关信息
    """

    def get(self, request, format=None):
        info = get_system_info()
        return Response(info)


class ResumeInfo(BaseAPIView):
    """
    返回 web 应用的相关信息
    """

    def get(self, request, format=None):
        info = get_resume_info()
        return Response(info)
