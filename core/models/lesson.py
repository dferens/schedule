from django.db import models
from django.db.models.query import QuerySet

from .course import Course
from .group import Group
from .teacher import Teacher


class LessonQuerySet(QuerySet):

    def of_group(self, group):
        return self.filter(groups=group)


class Lesson(models.Model):
    WEEK_CHOICES = (
        (1, 'перший'),
        (2, 'другий')
    )
    WEEKDAY_CHOICES = (
        (1, 'пн'),
        (2, 'вт'),
        (3, 'ср'),
        (4, 'чт'),
        (5, 'пт'),
        (6, 'сб'),
        (7, 'нд')
    )
    NUMBER_CHOICES = tuple(
        (n, str(n)) for n in range(1, 6)
    )
    TYPE_LECTURE = 'lecture'
    TYPE_LAB = 'lab'
    TYPE_PRACTICE = 'practice'
    TYPE_CHOICES = (
        (TYPE_LECTURE, 'лекція'),
        (TYPE_LAB, 'лаба'),
        (TYPE_PRACTICE, 'практика'),
    )
    course = models.ForeignKey(Course, verbose_name='курс')
    week = models.PositiveSmallIntegerField('тиждень', choices=WEEK_CHOICES)
    weekday = models.PositiveSmallIntegerField('день', choices=WEEKDAY_CHOICES)
    number = models.PositiveSmallIntegerField('пара', choices=NUMBER_CHOICES)
    place = models.CharField('аудиторія', max_length=10)
    type = models.CharField('тип заняття', max_length=16, choices=TYPE_CHOICES)
    teacher = models.ForeignKey(Teacher, verbose_name='викладач', null=True)
    groups = models.ManyToManyField(Group, verbose_name='групи')

    objects = LessonQuerySet.as_manager()

    class Meta:
        verbose_name = 'заняття'
        verbose_name_plural = 'заняття'
        unique_together = (
            ('course', 'week', 'weekday', 'number', 'place'),
        )
