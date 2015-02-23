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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('short_name', models.CharField(max_length=8, verbose_name='коротка назва')),
                ('full_name', models.CharField(max_length=128, verbose_name='повна назва')),
            ],
            options={
                'verbose_name_plural': 'курси',
                'verbose_name': 'курс',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('prefix', models.CharField(max_length=4, verbose_name='префікс')),
                ('code', models.CharField(unique=True, max_length=8, verbose_name='шифр')),
                ('okr', models.CharField(choices=[('bachelor', 'бакалаврат'), ('magister', 'магістратура'), ('specialist', 'спеціалісти')], max_length=16, verbose_name='освітньо-кваліфікаційний рівень')),
                ('type', models.CharField(choices=[('daily', 'денна'), ('extramural', 'заочна')], max_length=10, verbose_name='форма навчання')),
            ],
            options={
                'verbose_name_plural': 'групи',
                'verbose_name': 'група',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('week', models.PositiveSmallIntegerField(choices=[(1, 'перший'), (2, 'другий')], verbose_name='тиждень')),
                ('weekday', models.PositiveSmallIntegerField(choices=[(1, 'пн'), (2, 'вт'), (3, 'ср'), (4, 'чт'), (5, 'пт'), (6, 'сб'), (7, 'нд')], verbose_name='день')),
                ('number', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='пара')),
                ('place', models.CharField(max_length=10, verbose_name='аудиторія', null=True)),
                ('type', models.CharField(choices=[('lecture', 'лекція'), ('lab', 'лаба'), ('practice', 'практика')], max_length=16, verbose_name='тип заняття', null=True)),
                ('course', models.ForeignKey(to='core.Course', verbose_name='курс')),
                ('groups', models.ManyToManyField(to='core.Group', verbose_name='групи')),
            ],
            options={
                'verbose_name_plural': 'заняття',
                'verbose_name': 'заняття',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('short_name', models.CharField(max_length=64)),
                ('full_name', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name_plural': 'викладачі',
                'verbose_name': 'викладач',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(null=True, to='core.Teacher', verbose_name='викладач'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together=set([('course', 'week', 'weekday', 'number', 'place')]),
        ),
    ]
