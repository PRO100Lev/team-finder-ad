import io
import os
import random

from django import forms
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth import get_user_model

from team_finder.constants import LIMITS, MESSAGES, PALETTE


def validate_github_url(value):
    if value and "github.com" not in value:
        raise forms.ValidationError(MESSAGES["github_bad"])


def validate_phone(phone, instance=None):
    User = get_user_model()
    if phone.startswith("8"):
        phone = "+7" + phone[1:]
    elif not phone.startswith("+7"):
        raise forms.ValidationError(MESSAGES["phone_invalid"])

    if len(phone) != 12:
        raise forms.ValidationError(MESSAGES["phone_short"])

    if not phone[2:].isdigit():
        raise forms.ValidationError(MESSAGES["phone_nan"])

    other = User.objects.filter(phone=phone)
    if instance and instance.pk:
        other = other.exclude(pk=instance.pk)

    if other.exists():
        raise forms.ValidationError(MESSAGES["phone_taken"])

    return phone


def make_avatar(self):
    bg = random.choice(PALETTE["backgrounds"])
    letter = self.name[0].upper() if self.name else self.email[0].upper()
    canvas = Image.new("RGB", (LIMITS["avatar_size"], LIMITS["avatar_size"]), bg)
    draw = ImageDraw.Draw(canvas)

    font_file = os.path.join(
        settings.BASE_DIR,
        "static",
        "fonts",
        "Neue_Haas_Grotesk_Display_Pro_75_Bold.otf",
    )
    font = ImageFont.truetype(font_file, LIMITS["avatar_font"])
    box = draw.textbbox(PALETTE["origin"], letter, font=font)
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = (LIMITS["avatar_size"] - w) / 2 - box[0]
    y = (LIMITS["avatar_size"] - h) / 2 - box[1]
    draw.text((x, y), letter, fill=PALETTE["foreground"], font=font)
    stream = io.BytesIO()
    canvas.save(stream, format=PALETTE["image_type"])

    self.avatar.save(
        f"pic_{self.email}.png", ContentFile(stream.getvalue()), save=False
    )
