from django.db import models
from django.db.models.query import QuerySet

from ..utils.db import QuerySetMixin


class TeacherQuerySet(QuerySetMixin, QuerySet):
    pass


class Teacher(models.Model):
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=64)
    full_name = models.CharField(max_length=128)

    objects = TeacherQuerySet.as_manager()

    class Meta:
        verbose_name = 'викладач'
        verbose_name_plural = 'викладачі'

    def __str__(self):
        return self.full_name
