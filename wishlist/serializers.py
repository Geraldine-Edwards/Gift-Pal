from rest_framework import serializers
from .models import WishlistCategory, WishlistItem

class WishlistCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistCategory
        fields = ['id', 'name', 'slug', 'occasion_date', 'created_at']

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ['id', 'category', 'item_name', 'link', 'description', 'priority', 'reserved_by', 'created_at']

def create(self, validated_data):
    # Ensure the category is set
    category = validated_data.get('category')
    if not category:
        raise serializers.ValidationError("Category is required.")
    return super().create(validated_data)