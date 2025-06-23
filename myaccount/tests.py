from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class ProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='pass')
        self.client.login(username='profileuser', password='pass')

    def test_view_profile(self):
        response = self.client.get(reverse('myaccount:myaccount_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_edit_profile(self):
        response = self.client.post(reverse('myaccount:edit_profile'), {
            'username': 'profileuser',
            'first_name': 'NewName'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NewName')