from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.urls import reverse
from .models import Friendship
from .forms import AddFriendForm
from planner.models import Planner
from wishlist.models import WishlistItem

def friendship_list(request):
    friendships = Friendship.objects.filter(user=request.user, confirmed=True)
    pending_friendships = Friendship.objects.filter(friend=request.user, confirmed=False)
    form = AddFriendForm(user=request.user)
    
    search_query = request.GET.get('search_query', '').strip()
    search_results = []

    if search_query:
        search_results = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)[:5]

    return render(request, 'friendslist/friendslist.html', {
        'friendships': friendships,
        'pending_friendships': pending_friendships,
        'form': form,
        'search_results': search_results,
        'search_query': search_query,  # To keep the input field populated
    })

@login_required
def add_friend(request):
    if request.method == 'POST':
        friend_id = request.POST.get('friend_id')
        if friend_id:
            friend = User.objects.get(id=friend_id)
            Friendship.objects.create(user=request.user, friend=friend)
            messages.success(request, f"Friend request sent to {friend.username}.")
        else:
            messages.error(request, "Something went wrong. Please try again.")
        return redirect('friendslist')

@login_required
def friendsdetail(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    events = Planner.objects.filter(user=friend)
    wishlist_items = WishlistItem.objects.filter(user=friend)
    return render(request, 'friendslist/frienddetail.html', {
        'friend': friend,
        'events': events,
        'wishlist_items': wishlist_items
    })

@login_required
def confirm_friendship(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id, friend=request.user)
    if request.method == 'POST':
        friendship.confirmed = True
        friendship.save()
        return HttpResponseRedirect(reverse('friendslist'))
    return render(request, 'friendslist/confirm_friendship.html', {'friendship': friendship})

@login_required
def remove_friend(request, friend_id):
    """
    Removes a friendship between the logged-in user and the specified friend.
    """
    friend = get_object_or_404(User, id=friend_id)
    
    # Delete both directions of the friendship
    Friendship.objects.filter(user=request.user, friend=friend).delete()
    Friendship.objects.filter(user=friend, friend=request.user).delete()
    
    messages.success(request, f"You have removed {friend.username} from your friends.")
    return redirect('friendslist')  # Change to your actual friends list page name