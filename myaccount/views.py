from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MyAccount, Like
from .forms import ProfileImageForm, ProfileStatusForm, ProfileDetailsForm
from planner.models import Planner
from wishlist.models import WishlistItem

@login_required
def profile_view(request):
    myaccount, created = MyAccount.objects.get_or_create(user=request.user)

    status_form = ProfileStatusForm(instance=myaccount)
    details_form = ProfileDetailsForm(instance=myaccount)
    image_form = ProfileImageForm(instance=myaccount)

    if request.method == 'POST':
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            image_form = ProfileImageForm(request.POST, request.FILES, instance=myaccount)
            if image_form.is_valid():
                image_form.save()
                messages.success(request, 'Profile image updated successfully!')
                return redirect('myaccount:myaccount_home')

        # Handle status update
        elif 'status_message' in request.POST:
            status_form = ProfileStatusForm(request.POST, instance=myaccount)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, 'Status updated successfully!')
                return redirect('myaccount:myaccount_home')
            # Return response even if invalid
            return render(request, 'myaccount/profile.html', {
                'myaccount': myaccount,
                'image_form': image_form,
                'status_form': status_form,
                'details_form': details_form,
                'friends_count': request.user.friends.count(),
                'events_count': Planner.objects.filter(user=request.user).count(),
                'wishlist_items_count': WishlistItem.objects.filter(user=request.user).count()
            })

        # Handle profile details
        elif 'about_me' in request.POST:
            details_form = ProfileDetailsForm(request.POST, instance=myaccount)
            if details_form.is_valid():
                details_form.save()
                messages.success(request, 'Profile details updated successfully!')
                return redirect('myaccount:myaccount_home')
            # Return response even if invalid
            return render(request, 'myaccount/profile.html', {
                'myaccount': myaccount,
                'image_form': image_form,
                'status_form': status_form,
                'details_form': details_form,
                'friends_count': request.user.friends.count(),
                'events_count': Planner.objects.filter(user=request.user).count(),
                'wishlist_items_count': WishlistItem.objects.filter(user=request.user).count()
            })

    # GET request or no form submitted
    context = {
        'myaccount': myaccount,
        'image_form': image_form,
        'status_form': status_form,
        'details_form': details_form,
        'friends_count': request.user.friends.count(),
        'events_count': Planner.objects.filter(user=request.user).count(),
        'wishlist_items_count': WishlistItem.objects.filter(user=request.user).count()
    }
    return render(request, 'myaccount/profile.html', context)


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