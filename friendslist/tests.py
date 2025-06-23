from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Friendship

User = get_user_model()

class FriendshipTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.friend = User.objects.create_user(username='user2', password='pass')
        self.client.login(username='user1', password='pass')

    def test_send_friend_request(self):
        response = self.client.post(reverse('friends:add_friend'), {'friend_id': self.friend.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Friendship.objects.filter(user=self.user, friend=self.friend).exists())

    def test_accept_friend_request(self):
        Friendship.objects.create(user=self.friend, friend=self.user, status='pending')
        self.client.login(username='user2', password='pass')
        response = self.client.post(reverse('friends:accept_friend'), {'friend_id': self.user.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Friendship.objects.filter(user=self.friend, friend=self.user, status='accepted').exists())

    def test_remove_friend(self):
        Friendship.objects.create(user=self.user, friend=self.friend, status='accepted')
        response = self.client.post(reverse('friends:remove_friend'), {'friend_id': self.friend.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Friendship.objects.filter(user=self.user, friend=self.friend).exists())

# Create your tests here.
