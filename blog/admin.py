from django.contrib import admin

from blog.models import BlogPost, CategoriesPost


# Register your models here.
@admin.register(BlogPost)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "meta_description", "category")
    search_fields = ("title", )
    list_filter = ("status", )

@admin.register(CategoriesPost)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("name", )
    list_filter = ("name", )

