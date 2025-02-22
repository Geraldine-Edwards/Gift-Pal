from django.db import models
from django.contrib.auth.models import User
from wishlist.models import WishlistItem

class Planner(models.Model):
    user = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField (null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wishlist = models.ForeignKey(WishlistItem, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

