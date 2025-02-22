from django.contrib import admin
from .models import MyAccount

# Register your models here.
class MyAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_on')
    search_fields = ('user',)
    list_filter = ('user', 'updated_on')
    ordering = ('-updated_on',)

admin.site.register(MyAccount, MyAccountAdmin)