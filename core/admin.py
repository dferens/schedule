from django.contrib import admin
from django.contrib.admin import register, ModelAdmin
from django.core.urlresolvers import reverse

from . import models


class LessonInline(admin.TabularInline):
    model = models.Lesson
    max_num = 0


@register(models.Group)
class GroupAdmin(ModelAdmin):
    list_display = ('code', 'okr', 'type')
    ordering = ['code']
    radio_fields = {'type': admin.HORIZONTAL}


@register(models.Course)
class CourseAdmin(ModelAdmin):
    inlines = [LessonInline]
    list_display = ('short_name', 'full_name')
    list_display_links = ['short_name']
    ordering = ['short_name']


@register(models.Teacher)
class TeacherAdmin(ModelAdmin):
    inlines = [LessonInline]
    list_display = ('id', 'name', 'short_name', 'full_name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@register(models.Lesson)
class LessonAdmin(ModelAdmin):
    list_filter = ('week', 'weekday', 'number', 'type')
    list_display = (
        'course', 'type', 'teacher_link',
        'week', 'weekday', 'number', 'place'
    )
    radio_fields = {'week': admin.HORIZONTAL}

    def teacher_link(self, lesson):
        url = reverse('admin:core_teacher_change', args=[lesson.teacher_id])
        return '<a href="%s">%s</a>' % (url, lesson.teacher)
    teacher_link.allow_tags = True
    teacher_link.short_description = models.Teacher._meta.verbose_name
