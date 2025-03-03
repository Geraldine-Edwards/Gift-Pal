from django.contrib import admin
from .models import Friendship, FriendRequest


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'created_at')
    search_fields = ('user1__username', 'user2__username')
    list_filter = ('user1', 'user2', 'created_at')

def get_queryset(self, request):
        # Ensure friendships are displayed in a normalized order (user1.id < user2.id)
        return super().get_queryset(request).order_by('user1__id', 'user2__id')
    

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('status', 'created_at', 'updated_at', 'sender')
    list_editable = ('status',)  # Allow editing the status directly in the list view

    actions = ['mark_as_accepted', 'mark_as_declined']

    def mark_as_accepted(self, request, queryset):
        queryset.update(status='accepted')
    mark_as_accepted.short_description = "Mark selected requests as accepted"

    def mark_as_declined(self, request, queryset):
        queryset.update(status='declined')
    mark_as_declined.short_description = "Mark selected requests as declined"