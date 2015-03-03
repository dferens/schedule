from django import forms
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import View, TemplateView
from django.shortcuts import redirect, get_object_or_404

from . import service
from .models import Group, Teacher, Course


class ScheduleAppView(TemplateView):
    template_name = 'core/schedule.html'


class LessonsView(View):

    def get(self, request):
        params = request.GET

        if 'group' in params and len(params['group'].strip()) > 2:
            group = service.find_group(params['group'].strip())
            lessons = service.get_group_lessons(group)
        elif 'teacher' in params and params['teacher'].isdigit():
            teacher = get_object_or_404(Teacher, id=params['teacher'])
            lessons = service.get_teacher_lessons(teacher)
        elif 'course' in params and params['course'].isdigit():
            course = get_object_or_404(Course, id=params['course'])
            lessons = service.get_course_lessons(course)
        else:
            return HttpResponseBadRequest()

        return JsonResponse({
            'lessons': [{
                'course': {
                    'id': lesson.course.id,
                    'short_name': lesson.course.short_name,
                    'full_name': lesson.course.full_name
                },
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

