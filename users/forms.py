from django import forms
from django.contrib.auth import get_user_model

from team_finder.constants import LIMITS, MESSAGES

User = get_user_model()


class SignUpForm(forms.Form):
    name = forms.CharField(
        label='Имя',
        max_length=LIMITS['user_name'],
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    surname = forms.CharField(
        label='Фамилия',
        max_length=LIMITS['user_surname'],
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    email = forms.EmailField(
        label='Почта',
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    password = forms.CharField(
        label='Пароль',
        min_length=LIMITS['min_password'],
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(MESSAGES['email_taken'])
        return email

    def save(self):
        return User.objects.create_user(
            email=self.cleaned_data['email'],
            name=self.cleaned_data['name'],
            surname=self.cleaned_data['surname'],
            password=self.cleaned_data['password']
        )


class SignInForm(forms.Form):
    email = forms.EmailField(
        label='Почта',
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )


class EditProfileForm(forms.ModelForm):
    phone = forms.CharField(
        label='Телефон',
        max_length=LIMITS['user_phone'],
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'surname': forms.TextInput(attrs={'class': 'form-input'}),
            'avatar': forms.FileInput(attrs={'class': 'form-input'}),
            'about': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'github_url': forms.URLInput(attrs={'class': 'form-input'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone.startswith('8'):
            phone = '+7' + phone[1:]
        elif not phone.startswith('+7'):
            raise forms.ValidationError(MESSAGES['phone_invalid'])
        if len(phone) != 12:
            raise forms.ValidationError(MESSAGES['phone_short'])
        if not phone[2:].isdigit():
            raise forms.ValidationError(MESSAGES['phone_nan'])
        other = User.objects.filter(phone=phone).exclude(pk=self.instance.pk)
        if other.exists():
            raise forms.ValidationError(MESSAGES['phone_taken'])
        return phone

    def clean_github(self):
        url = self.cleaned_data.get('github_url', '')
        if url and 'github.com' not in url:
            raise forms.ValidationError(MESSAGES['github_bad'])
        return url


class ChangeSecretForm(forms.Form):
    current_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    new_password = forms.CharField(
        label='Новый пароль',
        min_length=LIMITS['min_password'],
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    repeat_password = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError(MESSAGES['wrong_password'])
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        repeat_password = cleaned_data.get('repeat_password')

        if new_password and new_password != repeat_password:
            raise forms.ValidationError(MESSAGES['password_mismatch'])
        return cleaned_data

    def save(self):
        self.user.set_password(self.cleaned_data['new_password'])
        self.user.save()
