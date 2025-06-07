import logging
import os

logger = logging.getLogger(__name__)

# stub for AI interaction
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
import logging
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import TelegramUser, Lead, LeadAnswer
from .serializers import LeadAnswerRequestSerializer, LeadAnswerResponseSerializer

logger = logging.getLogger(__name__)


# --- Core logic for dialog handling ---
def ai_handle_dialogue(lead, incoming_text):
    """
    Передаёт историю диалога в OpenAI и получает ответ:
      - reply_text
    """
    messages = [
        {"role": "system", "content": "Ты — квалификационный бот, собирающий данные о клиенте."}
    ]
    for ans in lead.answers.all().order_by('answered_at'):
        role = 'assistant' if ans.question_key == 'ai_reply' else 'user'
        messages.append({"role": role, "content": ans.answer})
    messages.append({"role": "user", "content": incoming_text})

    resp = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=150
    )
    return resp.choices[0].message.content.strip()

class LeadAnswerView(APIView):
    """Сохранить текст от пользователя, сгенерировать ответ AI"""
    def post(self, request, internal=False):
        serializer = LeadAnswerRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat_id = serializer.validated_data['chat_id']
        text = serializer.validated_data['text']

        user, _ = TelegramUser.objects.get_or_create(
            chat_id=chat_id,
            defaults={'first_name': '', 'last_name': '', 'username': ''}
        )
        lead, _ = Lead.objects.get_or_create(
            user=user,
            status='in_progress',
            defaults={'created_at': timezone.now()}
        )

        LeadAnswer.objects.create(lead=lead, question_key='user_message', answer=text)
        try:
            reply_text = ai_handle_dialogue(lead, text)
        except Exception as e:
            logger.error("AI error: %s", e)
            traceback.print_exc()
            if internal:
                return None
            return Response({"detail": f"Ошибка AI: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        LeadAnswer.objects.create(lead=lead, question_key='ai_reply', answer=reply_text)
        should_schedule = bool(lead.monthly_volume and lead.meeting_time_pref)
        data = {'reply_text': reply_text, 'should_schedule': should_schedule}

        return Response(data, status=status.HTTP_200_OK)

class TelegramWebhookView(APIView):
    """Принимает обновления от Telegram и отвечает пользователю"""
    def post(self, request):
        update = request.data
        message = update.get('message') or update.get('edited_message')
        if not message:
            return Response({'ok': True})
        chat_id = message['chat']['id']
        text = message.get('text', '')

        # Вызов основного эндпоинта logic-вью
        internal_req = type('Req', (), {'data': {'chat_id': chat_id, 'text': text}})()
        resp = LeadAnswerView().post(internal_req, internal=True)
        if resp is None:
            return Response({'ok': True})
        result = resp.data

        # Отправить сообщение обратно в Telegram
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        send_url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = {'chat_id': chat_id, 'text': result['reply_text']}
        try:
            requests.post(send_url, json=payload)
        except Exception as e:
            logger.error("Telegram send error: %s", e)

        return Response({'ok': True})

class ScheduleView(APIView):
    """Эндпоинт создания события в Google Calendar"""
    def post(self, request, lead_id):
        # TODO: реализовать логику создания события и сохранения CalendarEvent
        return Response({'detail': 'Not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)
