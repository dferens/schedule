# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('short_name', models.CharField(max_length=8, verbose_name='коротка назва')),
                ('full_name', models.CharField(max_length=128, verbose_name='повна назва')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курси',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('prefix', models.CharField(max_length=4, verbose_name='префікс')),
                ('code', models.CharField(max_length=8, verbose_name='шифр', unique=True)),
                ('okr', models.CharField(max_length=16, verbose_name='освітньо-кваліфікаційний рівень', choices=[('bachelor', 'бакалаврат'), ('magister', 'магістратура'), ('specialist', 'спеціалісти')])),
                ('type', models.CharField(max_length=10, verbose_name='форма навчання', choices=[('daily', 'денна'), ('extramural', 'заочна')])),
            ],
            options={
                'verbose_name': 'група',
                'verbose_name_plural': 'групи',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('week', models.PositiveSmallIntegerField(verbose_name='тиждень', choices=[(1, 'перший'), (2, 'другий')])),
                ('weekday', models.PositiveSmallIntegerField(verbose_name='день', choices=[(1, 'пн'), (2, 'вт'), (3, 'ср'), (4, 'чт'), (5, 'пт'), (6, 'сб'), (7, 'нд')])),
                ('number', models.PositiveSmallIntegerField(verbose_name='пара', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('type', models.CharField(max_length=16, verbose_name='тип заняття', choices=[('lecture', 'лекція'), ('lab', 'лаба'), ('practice', 'практика')])),
                ('place', models.CharField(max_length=10, verbose_name='аудиторія')),
                ('course', models.ForeignKey(verbose_name='курс', to='core.Course')),
                ('groups', models.ManyToManyField(verbose_name='групи', to='core.Group')),
            ],
            options={
                'verbose_name': 'заняття',
                'verbose_name_plural': 'заняття',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('short_name', models.CharField(max_length=64)),
                ('full_name', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'викладач',
                'verbose_name_plural': 'викладачі',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(verbose_name='викладач', to='core.Teacher', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together=set([('course', 'week', 'weekday', 'number')]),
        ),
    ]
