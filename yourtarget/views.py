from django.http import Http404
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic import ListView, DetailView

from blog.models import BlogPost, Services, Categories
from yourtarget.services import CacheMainPage


def contact_us(request):
    return render(request, "contact.html")

def not_found(request):
    return render(request, "404.html")

def about(request):
    return render(request, "about.html")


class MainPageView(ListView):
    model = BlogPost
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        print("⚡ get_cache_main_page запущен")
        return CacheMainPage.get_cache_main_page(self.request)



class ProductSearchView(ListView):
    """Класс для поиска продукта"""

    model = BlogPost
    template_name = "post_search.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("query")
        if query:
            return BlogPost.objects.filter(
                title__icontains=query
            )  # Поиск по названию продукта
            return context


class ServicesDetailView(DetailView):
    model = Services
    context_object_name = "service"
    slug_field = "slug"
    slug_url_kwarg = "slug"


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        return self.object


    def get_template_names(self):
        slug = self.kwargs.get('slug')
        template_name = f"{slug}.html"
        try:
            get_template(template_name)  # проверим наличие шаблона
        except Exception:
            raise Http404(f"No such template: {template_name}")
        return [template_name]