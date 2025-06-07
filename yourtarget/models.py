from django.db import models

class TelegramUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name or ''} @{self.username or self.chat_id}"

class Question(models.Model):
    key = models.SlugField(unique=True)   # 'business_type', 'automation_systems', 'monthly_volume', 'meeting_time_pref'
    text = models.TextField()

    def __str__(self):
        return self.key

class Lead(models.Model):
    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("scheduled", "Scheduled"),
    ]

    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="leads")
    created_at = models.DateTimeField(auto_now_add=True)

    business_type = models.TextField(null=True, blank=True)
    automation_systems = models.TextField(null=True, blank=True)
    monthly_volume = models.IntegerField(null=True, blank=True)
    meeting_time_pref = models.CharField(max_length=200, null=True, blank=True)

    summary = models.TextField(null=True, blank=True)  # итоговое описание лида
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in_progress")

    def __str__(self):
        return f"Lead {self.id} ({self.user})"

class LeadAnswer(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    question_key = models.CharField(max_length=100, blank=True)  # для AI-сгенерированных реплик можно хранить ключ 'ai_reply' или 'user_message'
    answer = models.TextField()
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question_key or self.question_id} @ {self.answered_at}"

class CalendarEvent(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="events")
    google_event_id = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.google_event_id} for Lead {self.lead.id}"
