from django import forms
from django.core.exceptions import ValidationError
from .models import Planner

class EventForm(forms.ModelForm):
    class Meta:
        model = Planner
        fields = ['title', 'start', 'end', 'description', 'color', 'reminder', 'wishlist', 'friends']
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reminder': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['wishlist'].queryset = self.user.wishlistitem_set.all()
            self.fields['friends'].queryset = self.user.friends.all()

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")

        # Only enforce that the end date must be after the start date
        if start and end and end < start:
            raise ValidationError("The end date must be after the start date.")

        return cleaned_data
