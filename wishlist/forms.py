from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import WishlistItem
import requests
from bs4 import BeautifulSoup


class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ['item_name', 'link', 'description', 'thumbnail_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('item_name', placeholder='Item name'),
            Field('link', placeholder='Link'),
            Field('description', placeholder='Description'),
            Field('thumbnail_url', placeholder='Thumbnail URL'),
        )
