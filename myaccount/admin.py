from django.contrib import admin
from .models import MyAccount, Like

# Register your models here.
class MyAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_on')
    search_fields = ('user',)
    list_filter = ('user', 'updated_on')
    ordering = ('-updated_on',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'event', 'wishlist_item', 'created_on')
    search_fields = ('user__username', 'friend__username', 'event__title', 'wishlist_item__item_name')
    list_filter = ('user', 'friend', 'event', 'wishlist_item', 'created_on')
    ordering = ('-created_on',)

admin.site.register(MyAccount, MyAccountAdmin)
admin.site.register(Like, LikeAdmin)