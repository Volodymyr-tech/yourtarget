from django.urls import path

from .api import LeadAnswerView, ScheduleView, TelegramWebhookView
from .views import about, MainPageView, ProductSearchView, ServicesDetailView, contact_us, not_found

app_name="yourtarget"

urlpatterns = [
    path('', MainPageView.as_view(), name='landing-index'),
    path('contact-us/', contact_us, name='contact-us'),
    path('404/', not_found, name='error404'),
    path('search/', ProductSearchView.as_view(), name='search'),
    path('service-detail/<slug:slug>/', ServicesDetailView.as_view(), name='service-detail'),
    path('about/', about, name='about'),
    path('api/leads/answer/', LeadAnswerView.as_view(), name='lead-answer'),
    path('telegram/webhook/', TelegramWebhookView.as_view(), name='telegram-webhook'),
    path('api/leads/<int:lead_id>/schedule/', ScheduleView.as_view(), name='lead-schedule'),
]
