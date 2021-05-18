from rest_framework import permissions
from rest_framework.views import APIView


class BaseAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    pass
