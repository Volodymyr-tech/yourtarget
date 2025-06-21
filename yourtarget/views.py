from django.http import Http404
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic import ListView, DetailView

from blog.models import BlogPost, Services, Categories
from yourtarget.services import CacheMainPage


# def index(request):
#     # позже сюда можно передавать любые данные: ссылки на бота, тексты и т.п.
#     context = {
#         'bot_link': 'https://t.me/bobwinchester_1',
#         'headline': 'Добро пожаловать! Получите консультацию в Telegram',
#         'description': 'Нажмите кнопку ниже, чтобы начать диалог с нашим AI-ассистентом'
#     }
#     return render(request, 'index.html', context)


def lifestyle(request):
    return render(request, "home-lifestyle-blog.html")


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
        else:
            context = {
         'message': 'Look like we dont have it'
     }
            return context


class ServicesDetailView(DetailView):
    model = Services
    context_object_name = "service"
   # template_name = 'web-dev.html'
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