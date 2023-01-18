from django.contrib import admin
from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'mobile', 'is_active', 'is_admin', 'is_staff', 'is_verified')
    list_filter = ('is_active', 'is_admin', 'is_staff', 'is_verified')
    search_fields = ('email', 'first_name', 'last_name', 'mobile')
    ordering = ('email', 'first_name', 'last_name', 'mobile', 'is_active', 'is_admin', 'is_staff', 'is_verified')
    
