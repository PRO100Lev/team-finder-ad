from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'name', 'surname', 'is_active']
    search_fields = ['email', 'name', 'surname']
    list_filter = ['is_active', 'is_staff']
