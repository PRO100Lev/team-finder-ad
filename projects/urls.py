from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.index, name="home"),
    path("list/", views.project_list, name="list"),
    path("create-project/", views.project_create, name="create"),
    path("<int:project_id>/", views.project_detail, name="detail"),
    path("<int:project_id>/edit/", views.project_edit, name="edit"),
    path("<int:project_id>/toggle-participate/", views.toggle_usership, name="toggle"),
    path("<int:project_id>/complete/", views.finish_project, name="finish"),
    path("skills/", views.skills_autocomplete, name="skills_autocomplete"),
    path("<int:project_id>/skills/add/", views.attach_skill, name="skill_add"),
    path(
        "<int:project_id>/skills/<int:skill_id>/remove/",
        views.detach_skill,
        name="skill_remove",
    ),
]
