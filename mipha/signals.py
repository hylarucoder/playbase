from django.db.models.signals import post_save
from django.dispatch import receiver

# Signal to save each new blog post instance into ElasticSearch
from yablog.models import BlogPost


@receiver(post_save, sender=BlogPost)
def index_post(sender, instance, **kwargs):
    instance.indexing()
