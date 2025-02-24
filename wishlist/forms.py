from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import WishlistItem, WishlistCategory
import requests
from bs4 import BeautifulSoup


class WishlistCategoryForm(forms.ModelForm):
    class Meta:
        model = WishlistCategory
        fields = ['name', 'occasion_date']  # Match model fields exactly
        widgets = {
            'occasion_date': forms.DateInput(attrs={'type': 'date'})
        }

class WishlistItemForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = WishlistCategory.objects.filter(user=user)
        
    class Meta:
        model = WishlistItem
        fields = ['category', 'item_name', 'link', 'description', 'thumbnail_url']
