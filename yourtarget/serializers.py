from rest_framework import serializers
from .models import TelegramUser, Lead, LeadAnswer

class LeadAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadAnswer
        fields = ('question_key', 'answer', 'answered_at')

class LeadAnswerRequestSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField()
    text = serializers.CharField()

class LeadAnswerResponseSerializer(serializers.Serializer):
    reply_text = serializers.CharField()
    should_schedule = serializers.BooleanField()