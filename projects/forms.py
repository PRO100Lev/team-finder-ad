from django import forms

from team_finder.constants import MESSAGES
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 6}),
            'github_url': forms.URLInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
        }
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'github_url': 'Репозиторий',
            'status': 'Состояние',
        }


def clean_github_url(self):
    url = self.cleaned_data.get('github_url', '')
    if url and 'github.com' not in url:
        raise forms.ValidationError(MESSAGES['github_bad'])
    return url
