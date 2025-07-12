from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)
    # token = models.CharField(
    #     max_length=100, verbose_name="Token", blank=True, null=True
    # )
    country = models.CharField(
        max_length=20,
        verbose_name="Страна проживания",
        help_text="Введите страну проживания",
        null=True,
        blank=True,
    )

    objects = CustomUserManager()  # Используем кастомный менеджер

    USERNAME_FIELD = "email"  # Указываем email вместо username
    REQUIRED_FIELDS = [
        "username",
    ]  # Поля, которые нужно запросить при создании суперюзера

    class Meta:
        verbose_name = "User"



    def __str__(self):
        return self.email