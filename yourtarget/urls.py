from django.urls import path

from .api import LeadAnswerView, ScheduleView, TelegramWebhookView
from .views import lifestyle, MainPageView, ProductSearchView, ServicesDetailView

app_name="yourtarget"

urlpatterns = [
    path('', MainPageView.as_view(), name='landing-index'),
    path('search/', ProductSearchView.as_view(), name='search'),
    path('service-detail/<slug:slug>/', ServicesDetailView.as_view(), name='service-detail'),
    path('lifestyle/', lifestyle, name='lifestyle'),
    path('api/leads/answer/', LeadAnswerView.as_view(), name='lead-answer'),
    path('telegram/webhook/', TelegramWebhookView.as_view(), name='telegram-webhook'),
    path('api/leads/<int:lead_id>/schedule/', ScheduleView.as_view(), name='lead-schedule'),
]
