from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import WishlistItem, WishlistCategory
from .forms import WishlistCategoryForm, WishlistItemForm


@login_required
def wishlist(request):
    categories = WishlistCategory.objects.filter(user=request.user)
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    add_category_form = WishlistCategoryForm(user=request.user)
    add_item_form = WishlistItemForm(user=request.user)
    return render(request, 'wishlist/wishlist.html', {
        'categories': categories,
        'wishlist_items': wishlist_items,
        'add_category_form': add_category_form,
        'add_item_form': add_item_form,
    })

@login_required
@require_POST
def add_category(request):
    form = WishlistCategoryForm(request.POST, user=request.user)
    if form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        category.save()
        return JsonResponse({
            'success': True,
            'category': {
                'id': category.id,
                'name': category.name,
            }
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@login_required
@require_POST
def edit_category(request, category_id):
    category = get_object_or_404(WishlistCategory, id=category_id, user=request.user)
    form = WishlistCategoryForm(request.POST, instance=category, user=request.user)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'category': {
                'id': category.id,
                'name': category.name,
            }
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@login_required
@require_POST
def delete_category(request, category_id):
    category = get_object_or_404(WishlistCategory, id=category_id, user=request.user)
    category.delete()
    return JsonResponse({'success': True})

@login_required
@require_POST
def add_wishlist_item(request):
    form = WishlistItemForm(request.POST, user=request.user)
    if form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return JsonResponse({
            'success': True,
            'item': {
                'id': item.id,
                'name': item.item_name,
                'description': item.description,
                'priority': item.get_priority_display(),
                'category_id': item.category.id,
            }
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'errors': 'Invalid request method'}, status=405)


@login_required
@require_POST
def edit_wishlist_item(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    form = WishlistItemForm(request.POST, instance=item, user=request.user)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'item': {
                'id': item.id,
                'name': item.item_name,
                'description': item.description,
                'priority': item.get_priority_display(),
            }
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@login_required
@require_POST
def delete_wishlist_item(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    item.delete()
    return JsonResponse({'success': True})

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
