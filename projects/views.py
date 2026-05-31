import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from team_finder.constants import MESSAGES, STATE
from team_finder.utils import pagination
from .forms import ProjectForm
from .models import Project, Skill


def index(request):
    return redirect('projects:list')


def project_list(request):
    projects = Project.objects.select_related('owner').all()

    skill_filter = request.GET.get('skill', '')
    all_skills = Skill.objects.all().order_by('name')

    if skill_filter:
        projects = projects.filter(skills__name=skill_filter)

    page = pagination(request, projects)

    return render(request, 'projects/project_list.html', {
        'projects': page,
        'all_skills': all_skills,
        'active_skill': skill_filter,
    })


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related('owner')
        .prefetch_related('participants', 'skills'),
        pk=project_id
    )
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect('projects:detail', project_id=project.pk)
    else:
        form = ProjectForm()

    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': False
    })


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:detail', project_id=project.pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': True,
        'project': project
    })


@login_required
@require_POST
def toggle_usership(request, project_id):
    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse(
            {'status': 'error', 'message': MESSAGES['project_missing']},
            status=HTTPStatus.NOT_FOUND
        )

    already_in = project.participants.filter(pk=request.user.pk).exists()

    if already_in:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return JsonResponse({
        'status': 'ok',
        'joined': not already_in
    })


def finish_project(request, project_id):
    project = Project.objects.filter(pk=project_id).first()

    if project is None:
        return JsonResponse(
            {'status': 'error', 'message': 'Проект не найден'},
            status=HTTPStatus.NOT_FOUND
        )

    if project.owner != request.user:
        return JsonResponse(
            {'status': 'error', 'message': 'Только автор может завершить проект'},
            status=HTTPStatus.FORBIDDEN
        )

    if project.status != STATE['active']:
        return JsonResponse(
            {'status': 'error', 'message': 'Проект уже завершён'},
            status=HTTPStatus.BAD_REQUEST
        )

    project.status = STATE['done']
    project.save()

    return JsonResponse({'status': 'ok', 'state': STATE['done']})


@require_GET
def skills_autocomplete(request):
    term = request.GET.get('q', '')
    if term:
        found = Skill.objects.filter(name__istartswith=term)[:10]
    else:
        found = Skill.objects.none()

    return JsonResponse(
        [{'id': s.id, 'name': s.name} for s in found],
        safe=False
    )


@login_required
@require_POST
def attach_skill(request, project_id):
    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse(
            {'error': MESSAGES['project_missing']},
            status=HTTPStatus.NOT_FOUND
        )

    if project.owner != request.user:
        return JsonResponse(
            {'error': MESSAGES['access_denied']},
            status=HTTPStatus.FORBIDDEN
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': MESSAGES['bad_json']},
            status=HTTPStatus.BAD_REQUEST
        )

    sid = data.get('skill_id')
    skill_title = data.get('name')
    created_at = False
    added = False

    if sid:
        skill = Skill.objects.filter(pk=sid).first()
        if skill is None:
            return JsonResponse(
                {'error': MESSAGES['skill_missing']},
                status=HTTPStatus.NOT_FOUND
            )
    elif skill_title:
        skill, created_at = Skill.objects.get_or_create(name=skill_title.strip())
    else:
        return JsonResponse(
            {'error': MESSAGES['skill_data_required']},
            status=HTTPStatus.BAD_REQUEST
        )

    if not project.skills.filter(pk=skill.pk).exists():
        project.skills.add(skill)
        added = True

    return JsonResponse({
        'skill_id': skill.pk,
        'name': skill.name,
        'created_at': created_at,
        'added': added,
    })


@login_required
@require_POST
def detach_skill(request, project_id, skill_id):
    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse(
            {'error': MESSAGES['project_missing']},
            status=HTTPStatus.NOT_FOUND
        )

    if project.owner != request.user:
        return JsonResponse(
            {'error': MESSAGES['access_denied']},
            status=HTTPStatus.FORBIDDEN
        )

    skill = Skill.objects.filter(pk=skill_id).first()
    if skill is None:
        return JsonResponse(
            {'error': MESSAGES['skill_missing']},
            status=HTTPStatus.NOT_FOUND
        )

    if project.skills.filter(pk=skill.pk).exists():
        project.skills.remove(skill)
        return JsonResponse({'status': 'ok'})

    return JsonResponse(
        {'error': MESSAGES['skill_not_present']},
        status=HTTPStatus.BAD_REQUEST
    )
