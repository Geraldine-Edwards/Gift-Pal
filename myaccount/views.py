from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MyAccount, Like
from .forms import ProfileImageForm
from planner.models import Planner
from wishlist.models import WishlistItem

@login_required
def profile_view(request):
    myaccount, created = MyAccount.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            myaccount.profile_image = form.cleaned_data['profile_image']  # Save Cloudinary file
            myaccount.save()
            messages.success(request, 'Your profile picture has been updated!')
            return redirect('myaccount:myaccount_home')
    else:
        form = ProfileImageForm()

    return render(request, 'myaccount/profile.html', {'myaccount': myaccount, 'form': form})



@login_required
def user_wishlist_view(request):
    myaccount, created = MyAccount.objects.get_or_create(user=request.user)
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'myaccount': myaccount, 'wishlist_items': wishlist_items})


@login_required
def like_event(request, event_id):
    event = get_object_or_404(Planner, id=event_id)
    like, created = Like.objects.get_or_create(user=request.user, event=event)
    if created:
        messages.success(request, 'You liked the event!')
    else:
        messages.info(request, 'You already liked this event.')
    return redirect('myaccount:profile')

@login_required
def like_wishlist_item(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id)
    like, created = Like.objects.get_or_create(user=request.user, wishlist_item=wishlist_item)
    if created:
        messages.success(request, 'You liked the wishlist item!')
    else:
        messages.info(request, 'You already liked this wishlist item.')
    return redirect('myaccount:profile')