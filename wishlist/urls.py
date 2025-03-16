from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WishlistCategoryViewSet, WishlistItemViewSet, wishlist

app_name='wishlist'

router = DefaultRouter()
router.register(r'categories', WishlistCategoryViewSet, basename='wishlistcategory')
router.register(r'items', WishlistItemViewSet, basename='wishlistitem')

urlpatterns = [
    path('', wishlist, name='wishlist'),
    path('api/', include(router.urls)),
]