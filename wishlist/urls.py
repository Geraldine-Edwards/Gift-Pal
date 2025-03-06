from django.urls import include, path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path('add/', views.add_wishlist_item, name='add_wishlist_item'),
    path('edit/<int:item_id>/', views.edit_wishlist_item, name='edit_wishlist_item'),
    path('delete/<int:item_id>/', views.delete_wishlist_item, name='delete_wishlist_item'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
]