from django.contrib import admin

from blog.models import BlogPost, Categories, Services


# Register your models here.
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "meta_description", "category")
    search_fields = ("title", )
    list_filter = ("status", )

@admin.register(Categories)
class CategoriesPostAdmin(admin.ModelAdmin):
    list_display = ("name", )
    list_filter = ("name", )

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ("name", "category", )
    list_filter = ("category",)