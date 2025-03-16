from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', oldviews.wishlist, name='wishlist'),
    path('add_category/', oldviews.add_category, name='add_category'),
    path('edit_category/<int:category_id>/', oldviews.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', oldviews.delete_category, name='delete_category'),
    path('add_item/', oldviews.add_wishlist_item, name='add_item'),
    path('edit_item/<int:item_id>/', oldviews.edit_wishlist_item, name='edit_item'),
    path('delete_item/<int:item_id>/', oldviews.delete_wishlist_item, name='delete_item'),
    path('reserve/<int:item_id>/', oldviews.reserve_item, name='reserve_item'),
]