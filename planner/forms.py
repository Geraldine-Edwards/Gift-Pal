from django import forms
from django.core.exceptions import ValidationError
from .models import Planner



class EventForm(forms.ModelForm):
    class Meta:
        model = Planner
        fields = ['title', 'start', 'end', 'description']

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")

        # Only enforce that the end date must be after the start date
        if start and end and end < start:
            raise ValidationError("The end date must be after the start date.")

        return cleaned_data
