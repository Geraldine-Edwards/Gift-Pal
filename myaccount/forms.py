from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import MyAccount

class ProfileImageForm(forms.Form):
    profile_image = CloudinaryFileField(
        options={'folder': 'profile_images'}
    )

class StatusMessageForm(forms.ModelForm):
    class Meta:
        model = MyAccount
        fields = ['status_message']
        widgets = {
            'status_message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Update your status message'}),
        }
