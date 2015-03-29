from django import forms
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import View, TemplateView
from django.shortcuts import redirect, get_object_or_404

from . import blocks
from .blocks import expand
from .. import service
from ..models import Group, Teacher, Course


class ScheduleAppView(TemplateView):
    template_name = 'core/schedule.html'


class SearchView(View):

    def get(self, request):
        query = request.REQUEST.get('query') or ''

        if len(query) > 1:
            results = service.search_objects(query)
        else:
            results = {'teachers': (), 'groups': (), 'courses': ()}

        data = {
            'results': {
                'groups': map(blocks.GroupBlock, results['groups']),
                'teachers': map(blocks.TeacherBlock, results['teachers']),
                'courses': map(blocks.CourseBlock, results['courses'])
            }
        }
        return JsonResponse(expand(data))


class BaseLessonsView(View):

    def get(self, request):
        form = self.form_class(request.REQUEST)

        if form.is_valid():
            context = expand(self.get_context_data(form))
            return JsonResponse(context)
        else:
            return HttpResponseBadRequest()


class GroupLessonsView(BaseLessonsView):

    class form_class(forms.Form):
        code = forms.CharField(min_length=2)

    def get_context_data(self, form):
        group = service.find_group(form.cleaned_data['code'])
        lessons = service.get_group_lessons(group)
        return {
            'group': blocks.GroupBlock(group),
            'schedule': blocks.ScheduleBlock(lessons)
        }


class CourseLessonsView(BaseLessonsView):

    class form_class(forms.Form):
        course = forms.ModelChoiceField(Course.objects.all())

    def get_context_data(self, form):
        course = form.cleaned_data['course']
        lessons = service.get_course_lessons(course)
        return {
            'course': blocks.CourseBlock(course),
            'schedule': blocks.ScheduleBlock(lessons)
        }


class TeacherLessonsView(BaseLessonsView):

    class form_class(forms.Form):
        teacher = forms.ModelChoiceField(Teacher.objects.all())

    def get_context_data(self, form):
        teacher = form.cleaned_data['teacher']
        lessons = service.get_teacher_lessons(teacher)
        return {
            'teacher': blocks.TeacherBlock(teacher),
            'schedule': blocks.ScheduleBlock(lessons)
        }
