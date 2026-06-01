from django.conf import settings
from django.db import models

from team_finder.constants import LIMITS, STATE, STATE_OPTIONS


class Skill(models.Model):
    name = models.CharField(
        max_length=LIMITS["skill_title"], unique=True, verbose_name="Название"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=LIMITS["project_title"], verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    github_url = models.URLField(blank=True, null=True, verbose_name="Репозиторий")
    status = models.CharField(
        max_length=LIMITS["status_field"],
        choices=STATE_OPTIONS,
        default=STATE["active"],
        verbose_name="Состояние",
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
        verbose_name="Участники",
    )
    skills = models.ManyToManyField(
        Skill, related_name="projects", blank=True, verbose_name="Требуемые навыки"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name
