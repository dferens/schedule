from django.db import models
from django.db.models.query import QuerySet

from ..utils.db import QuerySetMixin


class GroupQuerySet(QuerySetMixin, QuerySet):
    pass


class Group(models.Model):
    OKR_BACHELOR = 'bachelor'
    OKR_MAGISTER = 'magister'
    OKR_SPECIALIST = 'specialist'
    OKR_CHOICES = (
        (OKR_BACHELOR, 'бакалаврат'),
        (OKR_MAGISTER, 'магістратура'),
        (OKR_SPECIALIST, 'спеціалісти')
    )

    TYPE_DAILY = 'daily'
    TYPE_EXTRAMURAL = 'extramural'
    TYPE_CHOICES = (
        (TYPE_DAILY, 'денна'),
        (TYPE_EXTRAMURAL, 'заочна'),
    )

    prefix = models.CharField('префікс', max_length=4)
    code = models.CharField('шифр',
        max_length=8, unique=True
    )
    okr = models.CharField('освітньо-кваліфікаційний рівень',
        max_length=16, choices=OKR_CHOICES
    )
    type = models.CharField('форма навчання',
        max_length=10, choices=TYPE_CHOICES
    )

    objects = GroupQuerySet.as_manager()

    class Meta:
        verbose_name = 'група'
        verbose_name_plural = 'групи'

    def __str__(self):
        return self.code
