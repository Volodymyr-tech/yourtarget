from django.urls import path

from blog.views import cta, subscribe, CategoriesPostsListView
from blog.views import BlogDetailView, BlogPostListView

app_name = "blog"

urlpatterns = [
    path('all-posts/', BlogPostListView.as_view(), name='all_posts'),
    path('categories-posts/', CategoriesPostsListView.as_view(), name='categories_posts'),
    path('detail/<slug:slug>/', BlogDetailView.as_view(), name='detail'),
    path('subscribe/', subscribe, name='subscribe'),
    path('cta/', cta, name='cta')
]