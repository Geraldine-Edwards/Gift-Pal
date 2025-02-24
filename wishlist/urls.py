from django.urls import include, path
from .views import (
    wishlist_view,
    add_wishlist_item,
    edit_wishlist_item,
    delete_wishlist_item,
    WishlistCategoryCreateView,  
    WishlistCategoryUpdateView, 
    WishlistCategoryDeleteView
)

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_view, name='wishlist'),
    path('add/', add_wishlist_item, name='add_wishlist_item'),
    path('categories/add/', WishlistCategoryCreateView.as_view(), name='add_category'),
    path('categories/<int:pk>/edit/', WishlistCategoryUpdateView.as_view(), name='edit_category'),
    path('categories/<int:pk>/delete/', WishlistCategoryDeleteView.as_view(), name='delete_category'),
    path('edit/<int:item_id>/', edit_wishlist_item, name='edit_wishlist_item'),
    path('delete/<int:item_id>/', delete_wishlist_item, name='delete_wishlist_item'),
]