from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.constants import MESSAGES
from team_finder.utils import pagination
from .forms import ChangeSecretForm, EditProfileForm, SignInForm, SignUpForm

User = get_user_model()


def signup(request):
    if request.user.is_authenticated:
        return redirect('projects:list')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('projects:list')
    else:
        form = SignUpForm()

    return render(request, 'users/register.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('projects:list')

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('projects:list')
            form.add_error(None, MESSAGES['auth_failed'])
    else:
        form = SignInForm()

    return render(request, 'users/login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('projects:list')


def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/user-details.html', {'user': user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', user_id=request.user.pk)
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_secret(request):
    if request.method == 'POST':
        form = ChangeSecretForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            login(request, request.user)
            return redirect('users:profile', user_id=request.user.pk)
    else:
        form = ChangeSecretForm(request.user)

    return render(request, 'users/change_password.html', {'form': form})


def user_list(request):
    users = User.objects.filter(is_active=True)
    page = pagination(request, users)
    return render(request, 'users/participants.html', {'participants': page})
