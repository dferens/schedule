from django.db import models

from .group import Group


class Course(models.Model):
    group = models.ForeignKey(Group, verbose_name='група')
    short_name = models.CharField('коротка назва', max_length=8)
    full_name = models.CharField('повна назва', max_length=128)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курси'
        unique_together = (
            ('group', 'short_name'),
            ('group', 'full_name'),
        )

    def __str__(self):
        return self.full_name
