from django.contrib import admin

from users.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")
    search_fields = ("is_active", "is_staff", "first_name")