from blog.models import BlogPost, Categories, Services
from config.settings import CACHE_ENABLED
from django.core.cache import cache


class CacheMainPage:
    @staticmethod
    def get_cache_main_page(request):
        if CACHE_ENABLED:
            sessionid = request.sessionid
            print("anon_id:", sessionid)
            print(request.COOKIES)
            cache_key = f'cache_main_{sessionid}'
            cache_main_sessionid = cache.get(cache_key)

            if cache_main_sessionid is None:
                print("💾 Cache empty, making request to DB...")
                context = {
                "posts": list(BlogPost.objects.filter(status='PUBLISHED').order_by("-views")[:4]),
                "services_categories": list(Categories.objects.all()),
                "services": list(Services.objects.all())
                }
                cache.set(cache_key, context, 60 * 60)  # Cache for 1 hour
                return context

            return cache_main_sessionid
