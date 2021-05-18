from django.db.models.signals import post_save
from django.dispatch import receiver

from mipha.models import BlogPost


@receiver(post_save, sender=BlogPost)
def index_post(sender, instance, **kwargs):
    instance.indexing()
