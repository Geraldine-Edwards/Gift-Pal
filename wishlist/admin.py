from django.contrib import admin
from .models import WishlistItem

# Register your models here.
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'description', 'link', 'user')
    search_fields = ('item_name', 'user__username')
    list_filter = ('user',)
    ordering = ('item_name',)

admin.site.register(WishlistItem, WishlistItemAdmin)