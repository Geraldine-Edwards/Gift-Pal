from django.db import models
from django.contrib.auth.models import User
import requests


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.item_name


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
