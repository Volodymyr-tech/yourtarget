from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from blog.forms import SubscribeForm
from blog.models import BlogPost, Categories


# Create your views here.

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "post-layout-2.html"
    context_object_name = "blog_post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


    extra_context = {
        "categories": Categories.objects.all(),
        "popular_posts": BlogPost.objects.filter(status='PUBLISHED').order_by(
            "-views"
        )[:3]
    }


@require_POST
def subscribe(request):
    form = SubscribeForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))




class BlogPostListView(ListView):
    model = BlogPost
    template_name = "post-list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='PUBLISHED').order_by('-created_at')
        filter_param = self.request.GET.get("filter")  # Получаем параметр `filter`

        print("GET parameters:", self.request.GET)  # Логируем параметры

        print(filter_param)

        if filter_param:
            return queryset.filter(category=filter_param)
        else:
            return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Categories.objects.all()
        context["popular_posts"] = BlogPost.objects.filter(status='PUBLISHED').order_by("-views")[:3]
        return context


def cta(request):
    return render(request, "cta.html")



class CategoriesPostsListView(ListView):
    model = Categories
    template_name = 'post_categories.html'
    context_object_name = 'post_categories'


    def get_queryset(self):
        queryset = Categories.objects.all()
        return queryset
