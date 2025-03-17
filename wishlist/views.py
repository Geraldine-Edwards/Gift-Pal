from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import WishlistCategory, WishlistItem
from .serializers import WishlistCategorySerializer, WishlistItemSerializer

class WishlistCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistCategorySerializer
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can access

    def get_queryset(self):
        # Filter categories by the logged-in user
        return WishlistCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the logged-in user when creating a category
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()  # Save the updated category


class WishlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can access

    def get_queryset(self):
        # Filter items by the logged-in user
        return WishlistItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the logged-in user when creating an item
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()  # Save the updated category

# View for rendering the wishlist template
@login_required
def wishlist(request):
    categories = WishlistCategory.objects.filter(user=request.user).order_by('occasion_date')
    return render(request, 'wishlist/wishlist.html', {'categories': categories})