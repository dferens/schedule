from django.contrib.admin import register, ModelAdmin
from django.core.urlresolvers import reverse

from . import models


@register(models.Group)
class GroupAdmin(ModelAdmin):
    list_display = ('code', 'okr', 'type')


@register(models.Course)
class CourseAdmin(ModelAdmin):
    list_display = ('course_group', 'short_name', 'full_name')
    search_fields = ('full_name',)

    def course_group(self, course):
        return course.group.code
    course_group.short_description = models.Course._meta.get_field('group').verbose_name


@register(models.Teacher)
class TeacherAdmin(ModelAdmin):
    list_display = ('id', 'name', 'short_name', 'full_name')
    search_fields = ('name',)


@register(models.Lesson)
class LessonAdmin(ModelAdmin):
    list_filter = ('week', 'weekday', 'number', 'type', 'course__group')
    list_display = ('course_group', 'course', 'type', 'teacher_link', 'week', 'weekday', 'number')

    def course_group(self, lesson):
        return lesson.course.group.code
    course_group.short_description = models.Group._meta.verbose_name

    def teacher_link(self, lesson):
        url = reverse('admin:core_teacher_change', args=[lesson.teacher_id])
        return '<a href="%s">%s</a>' % (url, lesson.teacher)
    teacher_link.allow_tags = True
    teacher_link.short_description = models.Teacher._meta.verbose_name
