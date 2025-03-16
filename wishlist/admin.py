from django.contrib import admin
from .models import WishlistItem, WishlistCategory

class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'description', 'link', 'user', 'category', 'reserved_by')
    search_fields = ('item_name', 'user__username', 'category__name')
    list_filter = ('user', 'category')
    ordering = ('item_name',)

class WishlistCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'occasion_date', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('user',)
    ordering = ('name',)

admin.site.register(WishlistItem, WishlistItemAdmin)
admin.site.register(WishlistCategory, WishlistCategoryAdmin)