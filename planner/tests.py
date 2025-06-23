from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Planner

User = get_user_model()

class EventTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='eventuser', password='pass')
        self.client.login(username='eventuser', password='pass')

    def test_create_event(self):
        response = self.client.post(reverse('planner:event_create'), {
            'title': 'Party',
            'start': '2025-12-24T18:00',
            'end': '2025-12-24T23:00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(title='Party').exists())

    def test_edit_event(self):
        event = Event.objects.create(user=self.user, title='Old', start='2025-12-24T18:00', end='2025-12-24T23:00')
        response = self.client.post(reverse('planner:event_edit', args=[event.id]), {
            'title': 'New',
            'start': '2025-12-25T18:00',
            'end': '2025-12-25T23:00'
        })
        self.assertEqual(response.status_code, 302)
        event.refresh_from_db()
        self.assertEqual(event.title, 'New')

    def test_delete_event(self):
        event = Event.objects.create(user=self.user, title='Del', start='2025-12-24T18:00', end='2025-12-24T23:00')
        response = self.client.post(reverse('planner:event_delete', args=[event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Event.objects.filter(id=event.id).exists())
