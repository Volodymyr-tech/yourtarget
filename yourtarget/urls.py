from django.urls import path

from .api import LeadAnswerView, ScheduleView, TelegramWebhookView
from .views import index, lifestyle

app_name="yortarget"

urlpatterns = [
    path('', index, name='landing-index'),
    path('lifestyle/', lifestyle, name='lifestyle'),
    path('api/leads/answer/', LeadAnswerView.as_view(), name='lead-answer'),
    path('telegram/webhook/', TelegramWebhookView.as_view(), name='telegram-webhook'),
    path('api/leads/<int:lead_id>/schedule/', ScheduleView.as_view(), name='lead-schedule'),
]
