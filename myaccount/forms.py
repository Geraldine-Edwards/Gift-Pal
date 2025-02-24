from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import MyAccount

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = MyAccount
        fields = ['profile_image']

class ProfileStatusForm(forms.ModelForm):
    class Meta:
        model = MyAccount
        fields = ['status_message']
        widgets = {
            'status_message': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'How are you feeling today?'
            })
        }

class ProfileDetailsForm(forms.ModelForm):
    class Meta:
        model = MyAccount
        fields = ['about_me', 'birthday', 'favorite_links']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'about_me': forms.Textarea(attrs={'rows': 3}),
            'favorite_links': forms.TextInput(attrs={'class': 'form-control'})
        }