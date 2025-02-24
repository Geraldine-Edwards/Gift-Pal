from django.contrib import admin
from .models import Friendship


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'confirmed', 'created_at')
    search_fields = ('user', 'friend')
    list_filter = ('user', 'friend', 'confirmed')
    
    def save_model(self, request, obj, form, change):
            if change:  # If the object is being changed (not created)
                obj.clean()  # Run the clean method to validate the object
            super().save_model(request, obj, form, change)