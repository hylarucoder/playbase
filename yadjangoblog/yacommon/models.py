from django.conf import settings
from django.db import models


class Ownable(models.Model):
    """
    Abstract model that provides ownership of an object for a user.
    """

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              verbose_name="所有者", related_name="%(class)ss")

    class Meta:
        abstract = True

    def is_editable(self, request):
        """
        Restrict in-line editing to the objects's owner and superusers.
        """
        return request.user.is_superuser or request.user.id == self.owner_id


class Orderable(models.Model):
    order_num = models.IntegerField("排序", null=True)

    class Meta:
        abstract = True
