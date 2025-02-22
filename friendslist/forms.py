from django import forms
from django.contrib.auth.models import User
from .models import Friendship


class AddFriendForm(forms.Form):
    search_query = forms.CharField(
        label='Search Username',
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Search for a username', 'id': 'search_query'})
    )
    friend_username = forms.CharField(
        label='Friend Username',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': "Enter friend's username",
                               'list': 'username-suggestions', 'id': 'friend_username'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_friend_username(self):
        friend_username = self.cleaned_data['friend_username']
        if friend_username == self.user.username:
            raise forms.ValidationError("You cannot add yourself as a friend.")
        try:
            friend = User.objects.get(username=friend_username)
        except User.DoesNotExist:
            raise forms.ValidationError("User does not exist.")
        if Friendship.objects.filter(user=self.user, friend=friend).exists():
            raise forms.ValidationError("You are already friends with this user.")
        if Friendship.objects.filter(user=friend, friend=self.user).exists():
            raise forms.ValidationError("You are already friends with this user.")
        return friend_username
