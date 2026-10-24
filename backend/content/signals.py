"""Cheap editorial invalidation only. Never performs article analysis in a signal."""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import TopicAlias


@receiver(post_save, sender=TopicAlias)
@receiver(post_delete, sender=TopicAlias)
def alias_changed(sender, instance, raw=False, **kwargs):
    if raw: return
    from .services.connections import queue_connections
    queue_connections()
