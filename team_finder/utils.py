from django.core.paginator import Paginator
from django import forms
from PIL import Image, ImageDraw, ImageFont

from team_finder.constants import LIMITS


def pagination(request, data, per_page=None):
    if per_page is None:
        per_page = LIMITS["per_page"]

    pager = Paginator(data, per_page)
    current_page = request.GET.get("page", 1)
    return pager.get_page(current_page)
