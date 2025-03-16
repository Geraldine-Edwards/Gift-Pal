from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import requests
from bs4 import BeautifulSoup

app_name = 'wishlist'

class WishlistCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=65, unique=True, blank=True)
    occasion_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Wishlist Categories"
        ordering = ['-occasion_date']
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = f"{self.user.id}-{base_slug}"  # Include user ID in the slug
            # Ensure the slug does not exceed 65 characters
            if len(unique_slug) > 65:
                unique_slug = unique_slug[:65]
            self.slug = unique_slug
        super().save(*args, **kwargs)

class WishlistItem(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(WishlistCategory, on_delete=models.SET_NULL, 
                                null=True, blank=True)
    item_name = models.CharField(max_length=200)
    link = models.URLField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    reserved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reserved_items')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.item_name} ({self.user.username})"


def fetch_thumbnail_url(self, url):
    """
        Fetches the thumbnail URL from the provided web page URL.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try to fetch the Open Graph image tag
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
        
        # Fallback: Try to fetch the first image in the page
        first_image = soup.find('img')
        if first_image and first_image.get('src'):
                return first_image['src']
        
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Error fetching thumbnail: {e}")
    return None

def save(self, *args, **kwargs):
    """
        Automatically fetch and save the thumbnail URL when a link is provided.
    """
    if not self.thumbnail_url and self.link:
        self.thumbnail_url = self.fetch_thumbnail_url(self.link)
    super().save(*args, **kwargs)
