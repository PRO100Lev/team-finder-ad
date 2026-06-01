from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from team_finder.constants import LIMITS
from .managers import UserManager
from .utils import make_avatar


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Почта")
    name = models.CharField(max_length=LIMITS["user_name"], verbose_name="Имя")
    surname = models.CharField(
        max_length=LIMITS["user_surname"], verbose_name="Фамилия"
    )
    avatar = models.ImageField(upload_to="pictures/", verbose_name="Аватар")
    phone = models.CharField(max_length=LIMITS["user_phone"], verbose_name="Телефон")
    github_url = models.URLField(blank=True, verbose_name="GitHub")
    about = models.TextField(
        max_length=LIMITS["user_bio"], blank=True, verbose_name="О себе"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        ordering = ["id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.avatar:
            make_avatar(self)
        super().save(*args, **kwargs)
