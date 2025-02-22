from django.urls import path
from .views import profile_view, user_wishlist_view


app_name = 'myaccount'

urlpatterns = [
    path('', profile_view, name='myaccount_home'),
    path('wishlist/', user_wishlist_view, name='myaccount_wishlist'),
]