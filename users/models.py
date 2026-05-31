import io
import os
import random

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from team_finder.constants import LIMITS, PALETTE
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name='Почта'
    )
    name = models.CharField(
        max_length=LIMITS['user_name'],
        verbose_name='Имя'
    )
    surname = models.CharField(
        max_length=LIMITS['user_surname'],
        verbose_name='Фамилия'
    )
    avatar = models.ImageField(
        upload_to='pictures/',
        verbose_name='Аватар'
    )
    phone = models.CharField(
        max_length=LIMITS['user_phone'],
        verbose_name='Телефон'
    )
    github_url = models.URLField(
        blank=True,
        verbose_name='GitHub'
    )
    about = models.TextField(
        max_length=LIMITS['user_bio'],
        blank=True, 
        verbose_name='О себе'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Администратор'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def make_avatar(self):
        bg = random.choice(PALETTE['backgrounds'])
        letter = self.name[0].upper() if self.name else self.email[0].upper()
        canvas = Image.new('RGB', (LIMITS['avatar_size'], LIMITS['avatar_size']), bg)
        draw = ImageDraw.Draw(canvas)

        font_file = os.path.join(
            settings.BASE_DIR, 'static', 'fonts',
            'Neue_Haas_Grotesk_Display_Pro_75_Bold.otf'
        )
        font = ImageFont.truetype(font_file, LIMITS['avatar_font'])
        box = draw.textbbox(PALETTE['origin'], letter, font=font)
        w = box[2] - box[0]
        h = box[3] - box[1]
        x = (LIMITS['avatar_size'] - w) / 2 - box[0]
        y = (LIMITS['avatar_size'] - h) / 2 - box[1]
        draw.text((x, y), letter, fill=PALETTE['foreground'], font=font)
        stream = io.BytesIO()
        canvas.save(stream, format=PALETTE['image_type'])

        self.avatar.save(
            f'pic_{self.email}.png',
            ContentFile(stream.getvalue()),
            save=False
        )

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.make_avatar()
        super().save(*args, **kwargs)