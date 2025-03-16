from django import forms
from .models import WishlistItem, WishlistCategory
from django.contrib.auth.models import User



class WishlistCategoryForm(forms.ModelForm):
    class Meta:
        model = WishlistCategory
        fields = ['name', 'occasion_date'] 
        widgets = {
            'occasion_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance

class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ['category', 'item_name', 'link', 'description', 'priority']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = WishlistCategory.objects.filter(user=user)
