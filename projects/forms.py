from django import forms

from team_finder.constants import LIMITS
from .models import Project
from .utils import validate_github_url


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(
                attrs={"class": "form-input", "rows": LIMITS["form_rows"]}
            ),
            "github_url": forms.URLInput(attrs={"class": "form-input"}),
            "status": forms.Select(attrs={"class": "form-input"}),
        }
        labels = {
            "name": "Название",
            "description": "Описание",
            "github_url": "Репозиторий",
            "status": "Состояние",
        }


def clean_github_url(self):
    url = self.cleaned_data.get("github_url", "")
    validate_github_url(url)
    return url
