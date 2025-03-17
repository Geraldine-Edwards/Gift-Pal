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

    # Custom action to move items to "Uncategorized" and delete the category
    @action(detail=True, methods=['post'])
    def move_items_to_uncategorized(self, request, pk=None):
        category = self.get_object()  # Get the category to be deleted

        # Find or create an "Uncategorized" category for the user
        uncategorized_category, created = WishlistCategory.objects.get_or_create(
            user=request.user,
            name="Uncategorized",
            defaults={'occasion_date': None}  # Optional: Set a default occasion date
        )

        # Move all items to the "Uncategorized" category
        WishlistItem.objects.filter(category=category).update(category=uncategorized_category)

        # Delete the original category
        category.delete()

        return Response({'success': True}, status=status.HTTP_200_OK)
    

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