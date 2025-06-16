from django.urls import path

from blog.views import cta, subscribe
from blog.views import BlogDetailView, BlogPostListView

app_name = "blog"

urlpatterns = [
    path('all-posts/', BlogPostListView.as_view(), name='all_posts'),
    path('detail/<slug:slug>/', BlogDetailView.as_view(), name='detail'),
    path('subscribe/', subscribe, name='subscribe'),
    path('cta/', cta, name='cta')
]