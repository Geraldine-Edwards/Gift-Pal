from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import WishlistCategory, WishlistItem

User = get_user_model()

class WishlistCategoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='catuser', password='pass')
        self.client.login(username='catuser', password='pass')

    def test_create_category(self):
        response = self.client.post(reverse('wishlist:category_create'), {
            'name': 'Birthday',
            'occasion_date': '2025-12-25'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(WishlistCategory.objects.filter(name='Birthday').exists())

    def test_edit_category(self):
        category = WishlistCategory.objects.create(user=self.user, name='EditMe')
        response = self.client.post(reverse('wishlist:category_edit', args=[category.id]), {
            'name': 'Edited',
            'occasion_date': '2025-12-31'
        })
        self.assertEqual(response.status_code, 302)
        category.refresh_from_db()
        self.assertEqual(category.name, 'Edited')

    def test_delete_category(self):
        category = WishlistCategory.objects.create(user=self.user, name='DeleteMe')
        response = self.client.post(reverse('wishlist:category_delete', args=[category.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(WishlistCategory.objects.filter(id=category.id).exists())

class WishlistItemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='itemuser', password='pass')
        self.category = WishlistCategory.objects.create(user=self.user, name='Cat')
        self.client.login(username='itemuser', password='pass')

    def test_create_item(self):
        response = self.client.post(reverse('wishlist:item_create'), {
            'category': self.category.id,
            'item_name': 'Gift',
            'priority': 'medium'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(WishlistItem.objects.filter(item_name='Gift').exists())

    def test_edit_item(self):
        item = WishlistItem.objects.create(user=self.user, category=self.category, item_name='Old')
        response = self.client.post(reverse('wishlist:item_edit', args=[item.id]), {
            'category': self.category.id,
            'item_name': 'New',
            'priority': 'high'
        })
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.item_name, 'New')

    def test_delete_item(self):
        item = WishlistItem.objects.create(user=self.user, category=self.category, item_name='Del')
        response = self.client.post(reverse('wishlist:item_delete', args=[item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(WishlistItem.objects.filter(id=item.id).exists())