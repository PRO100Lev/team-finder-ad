from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.signup, name='register'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('list/', views.user_list, name='list'),
    path('<int:user_id>/', views.user_profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('password/', views.change_secret, name='change_password'),
]
