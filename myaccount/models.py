from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from planner.models import Planner
from wishlist.models import WishlistItem 

class MyAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField('image', null=True, blank=True)
    status_message = models.CharField(max_length=255, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    favorite_links = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    event = models.ForeignKey(Planner, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
    wishlist_item = models.ForeignKey(WishlistItem, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event', 'wishlist_item')

    def __str__(self):
        if self.event:
            return f"{self.user.username} likes {self.event.title}"
        elif self.wishlist_item:
            return f"{self.user.username} likes {self.wishlist_item.item_name}"
        return f"{self.user.username} likes an item"