from django import forms

from team_finder.constants import MESSAGES


def validate_github_url(value):
    if value and "github.com" not in value:
        raise forms.ValidationError(MESSAGES["github_bad"])
