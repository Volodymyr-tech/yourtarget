from blog.models import BlogPost, Categories



queryset = Categories.objects.select_related('blogposts').all()

for category in queryset:
    print(f"Category: {category.name}")