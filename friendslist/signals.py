from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Friendship

@receiver(post_delete, sender=Friendship)
def delete_reciprocal_friendship(sender, instance, **kwargs):
    """
    When a friendship is deleted, also delete the reciprocal friendship.
    """
    Friendship.objects.filter(user=instance.friend, friend=instance.user).delete()