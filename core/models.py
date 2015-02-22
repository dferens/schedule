from django.db import models


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

    class Meta:
        verbose_name = 'група'
        verbose_name_plural = 'групи'

    def __str__(self):
        return self.code


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


class Teacher(models.Model):
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=64)
    full_name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'викладач'
        verbose_name_plural = 'викладачі'

    def __str__(self):
        return self.full_name


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
    type = models.CharField('тип заняття',
        max_length=16, choices=TYPE_CHOICES
    )
    teacher = models.ForeignKey(Teacher, verbose_name='викладач', null=True)
    week = models.PositiveSmallIntegerField('тиждень', choices=WEEK_CHOICES)
    weekday = models.PositiveSmallIntegerField('день', choices=WEEKDAY_CHOICES)
    number = models.PositiveSmallIntegerField('пара', choices=NUMBER_CHOICES)

    class Meta:
        verbose_name = 'заняття'
        verbose_name_plural = 'заняття'
        unique_together = (
            ('course', 'week', 'weekday', 'number'),
        )
