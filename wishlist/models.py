from django.db import models
from django.contrib.auth.models import User
import requests

app_name = 'wishlist'

class WishlistCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    occasion_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Wishlist Categories"
        ordering = ['-occasion_date']

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(WishlistCategory, on_delete=models.SET_NULL, 
                                null=True, blank=True)
    item_name = models.CharField(max_length=200)
    link = models.URLField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.item_name} ({self.user.username})"


def fetch_thumbnail_url(self, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        # Parse the response to find the Open Graph image URL
        start = response.text.find(
            '<meta property="og:image" content="') + len('<meta property="og:image" content="')
        end = response.text.find('"', start)
        og_image_url = response.text[start:end]
        return og_image_url
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Error fetching thumbnail: {e}")
    return ''

def save(self, *args, **kwargs):
    if not self.thumbnail_url and self.link:
        self.thumbnail_url = self.fetch_thumbnail_url(self.link)
    super().save(*args, **kwargs)
