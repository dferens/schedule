from django.db import models


class Course(models.Model):
    short_name = models.CharField('коротка назва', max_length=8)
    full_name = models.CharField('повна назва', max_length=128)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курси'

    def __str__(self):
        return self.full_name
