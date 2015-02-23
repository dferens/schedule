from django.contrib.admin import register, ModelAdmin
from django.core.urlresolvers import reverse

from . import models


@register(models.Group)
class GroupAdmin(ModelAdmin):
    list_display = ('code', 'okr', 'type')


@register(models.Teacher)
class TeacherAdmin(ModelAdmin):
    list_display = ('id', 'name', 'short_name', 'full_name')
    search_fields = ('name',)


@register(models.Lesson)
class LessonAdmin(ModelAdmin):
    readonly_fields = ('course',)
    fields = ('course', 'week', 'weekday', 'number', 'place', 'type', 'groups')
    list_filter = ('week', 'weekday', 'number', 'type')
    list_display = (
        'course', 'type', 'teacher_link',
        'week', 'weekday', 'number', 'place'
    )

    def teacher_link(self, lesson):
        url = reverse('admin:core_teacher_change', args=[lesson.teacher_id])
        return '<a href="%s">%s</a>' % (url, lesson.teacher)
    teacher_link.allow_tags = True
    teacher_link.short_description = models.Teacher._meta.verbose_name
