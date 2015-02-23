from django.db import models
from django.db.models.query import QuerySet


class CourseQuerySet(QuerySet):

    def of_group(self, group):
        return self.filter(lesson__groups=group).distinct()


class Course(models.Model):
    short_name = models.CharField('коротка назва', max_length=8)
    full_name = models.CharField('повна назва', max_length=128)

    objects = CourseQuerySet.as_manager()

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курси'

    def __str__(self):
        return self.full_name
