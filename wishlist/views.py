from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import WishlistItem, WishlistCategory
from .forms import WishlistCategoryForm, WishlistItemForm


@login_required
def wishlist(request):
    categories = WishlistCategory.objects.filter(user=request.user)
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {
        'categories': categories,
        'wishlist_items': wishlist_items,
    })

@login_required
def add_category(request):
    if request.method == 'POST':
        form = WishlistCategoryForm(request.POST, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Category added successfully!')
            return redirect('wishlist:wishlist')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = WishlistCategoryForm(user=request.user)
    return render(request, 'wishlist/add_category.html', {'form': form})

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(WishlistCategory, id=category_id, user=request.user)
    if request.method == 'POST':
        form = WishlistCategoryForm(request.POST, instance=category, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('wishlist:wishlist')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = WishlistCategoryForm(instance=category, user=request.user)
    return render(request, 'wishlist/edit_category.html', {'form': form, 'category': category})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(WishlistCategory, id=category_id, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('wishlist:wishlist')
    return render(request, 'wishlist/delete_category.html', {'category': category})

@login_required
def add_wishlist_item(request):
    if request.method == 'POST':

        print("POST data:", request.POST)  # Debugging: Print POST data

        form = WishlistItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Wishlist item added successfully!')
            return redirect('wishlist:wishlist')
        else:

            print("Form errors:", form.errors)  # Debugging: Print form errors

            messages.error(request, 'Please correct the errors below.')
    else:
        form = WishlistItemForm(user=request.user)
    return render(request, 'wishlist/add_wishlist_item.html', {'form': form})


@login_required
def edit_wishlist_item(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    if request.method == 'POST':
        form = WishlistItemForm(request.POST, instance=item, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Wishlist item updated successfully!')
            return redirect('wishlist:wishlist')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = WishlistItemForm(instance=item, user=request.user)
    return render(request, 'wishlist/edit_wishlist_item.html', {'form': form, 'item': item})


@login_required
def delete_wishlist_item(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Wishlist item deleted successfully!')
        return redirect('wishlist:wishlist')
    return render(request, 'wishlist/delete_wishlist_item.html', {'item': item})

@login_required
def reserve_item(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id)
    
    # Check if the item is already reserved
    if item.reserved_by:
        messages.warning(request, f'This item is already reserved by {item.reserved_by.username}.')
    else:
        # Reserve the item for the current user
        item.reserved_by = request.user
        item.save()
        messages.success(request, f'You have reserved "{item.item_name}".')
    
    # Redirect back to the friend's detail page
    return redirect('friendslist:friendsdetail', friend_id=item.user.id)
