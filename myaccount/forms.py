from django import forms
from cloudinary.forms import CloudinaryFileField

class ProfileImageForm(forms.Form):
    profile_image = CloudinaryFileField(
        options={'folder': 'profile_images'}
    )
