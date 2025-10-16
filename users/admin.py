from django.contrib import admin
from .models import User, Team


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'age', 'gender', 'is_child']
    list_filter = ['gender', 'age']
    search_fields = ['username', 'first_name', 'last_name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'member_count', 'created_at']
    filter_horizontal = ['members']
    search_fields = ['name']
