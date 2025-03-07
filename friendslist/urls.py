from django.urls import path
from . import views


app_name = 'friendslist'

urlpatterns = [
    
    # Friend Requests
    path('send-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline-request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),

    # Friends List
    path('friends/', views.friend_requests, name='friendslist'),  # Main friends page
    path('friends/<int:friend_id>/', views.friendsdetail, name='friendsdetail'),  # Friend's profile
    path('remove-friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),  # Remove friend

    # Like Firend's Events & Wishlist Items
    path('event/<int:event_id>/like/', views.like_event, name='like_event'),
    path('wishlist/<int:item_id>/like/', views.like_wishlist_item, name='like_wishlist_item'),
]
