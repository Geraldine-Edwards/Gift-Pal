from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import WishlistItem, WishlistCategory
from .forms import WishlistItemForm, WishlistCategoryForm 


class WishlistCategoryCreateView(CreateView):
    model = WishlistCategory
    form_class = WishlistCategoryForm
    template_name = 'wishlist/category_form.html'
    success_url = reverse_lazy('wishlist:wishlist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WishlistCategoryUpdateView(UpdateView):
    model = WishlistCategory
    form_class = WishlistCategoryForm
    template_name = 'wishlist/category_form.html'
    success_url = reverse_lazy('wishlist:wishlist')

class WishlistCategoryDeleteView(DeleteView):
    model = WishlistCategory
    success_url = reverse_lazy('wishlist:wishlist')
    template_name = 'wishlist/category_confirm_delete.html'


@login_required
def wishlist_view(request):
    categories = WishlistCategory.objects.filter(user=request.user).prefetch_related('wishlistitem_set')
    uncategorized = WishlistItem.objects.filter(user=request.user, category__isnull=True)
    return render(request, 'wishlist/wishlist.html', {
        'categories': categories,
        'uncategorized': uncategorized
    })

@login_required
def add_wishlist_item(request):
    if request.method == 'POST':
        form = WishlistItemForm(request.user, request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Item added successfully!')
            return redirect('wishlist:wishlist')
    else:
        form = WishlistItemForm(request.user)
    return render(request, 'wishlist/wishlistitem_form.html', {'form': form})


@login_required
def edit_wishlist_item(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    if request.method == 'POST':
        form = WishlistItemForm(request.POST, instance=wishlist_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wishlist item updated successfully!')
            return redirect('wishlist:wishlist')
    else:
        form = WishlistItemForm(instance=wishlist_item)
    return render(request, 'wishlist/wishlistitem_form.html', {'form': form})


@login_required
def delete_wishlist_item(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    if request.method == 'POST':
        wishlist_item.delete()
        messages.success(request, 'Wishlist item deleted successfully!')
        return redirect('wishlist:wishlist')
    return render(request, 'wishlist/delete_wishlist_item.html', {'wishlist_item': wishlist_item})
