from django.contrib import admin
from .models import Planner


@admin.register(Planner)
class PlannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'start', 'end')
    search_fields = ('title', 'user')
    list_filter = ('user', 'start', 'end')
    ordering = ('start', 'end')


