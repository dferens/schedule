from django import forms
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import View, TemplateView
from django.shortcuts import redirect, get_object_or_404

from . import service
from .models import Group, Teacher


class ScheduleAppView(TemplateView):
    template_name = 'core/schedule.html'


class LessonsView(View):

    def get(self, request):
        params = request.GET

        if 'group' in params and len(params['group']) > 2:
            group = service.find_group(params['group'])
            lessons = service.get_group_lessons(group)
        elif 'teacher' in params and params['teacher'].isdigit():
            teacher = get_object_or_404(Teacher, id=params['teacher'])
            lessons = service.get_teacher_lessons(teacher)
        else:
            return HttpResponseBadRequest()

        return JsonResponse({
            'lessons': [{
                'week': lesson.week,
                'weekday': lesson.weekday,
                'number': lesson.number,
                'place': lesson.place,
                'type': lesson.type,
                'teacher': {
                    'id': lesson.teacher_id,
                    'short_name': lesson.teacher.short_name
                } if lesson.teacher else None,
                'groups': list(lesson.groups.values_list('code', flat=True))
            } for lesson in lessons]
        })
