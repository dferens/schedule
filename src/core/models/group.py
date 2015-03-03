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

    @staticmethod
    def autocomplete_search_fields():
        return ['code__icontains']


class GroupIndexManager(models.Manager):

    def lookup_group(self, group_alias):
        try:
            return (
                self.select_related('group')
                    .get(alias__iexact=group_alias)
                    .group
            )
        except self.model.DoesNotExist:
            return None

    def add_alias(self, group, alias):
        self.get_or_create(group=group, alias=alias)


class GroupIndex(models.Model):
    alias = models.CharField(max_length=8)
    group = models.ForeignKey(Group)

    objects = GroupIndexManager()

    class Meta:
        unique_together = (
            ('alias', 'group'),
        )
