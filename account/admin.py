from django.contrib import admin
from .models import User
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role']
    list_filter = ['id', 'email', 'role']
    search_fields = ['username', 'email', 'role']
