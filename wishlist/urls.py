from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WishlistCategoryViewSet, WishlistItemViewSet, wishlist

app_name='wishlist'

router = DefaultRouter()
router.register(r'categories', WishlistCategoryViewSet, basename='category')
router.register(r'items', WishlistItemViewSet, basename='item')

urlpatterns = [
    path('api/', include(router.urls)),  # Include the router URLs
    path('', wishlist, name='wishlist'),
]