from django.db import models
from django.db.models.query import QuerySet


class SiteSettingsQuerySet(QuerySet):

    def get(self):
        return self.all()[0]


class SiteSettings(models.Model):
    first_week_monday = models.DateField()

    objects = SiteSettingsQuerySet.as_manager()

    class Meta:
        verbose_name = u'Налаштування сайту'
        verbose_name_plural = verbose_name
