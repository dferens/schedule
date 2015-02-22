from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=64)
    full_name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'викладач'
        verbose_name_plural = 'викладачі'

    def __str__(self):
        return self.full_name
