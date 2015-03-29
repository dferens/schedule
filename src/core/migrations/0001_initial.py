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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('prefix', models.CharField(max_length=4, verbose_name='префікс')),
                ('code', models.CharField(unique=True, max_length=8, verbose_name='шифр')),
                ('okr', models.CharField(max_length=16, choices=[('bachelor', 'бакалаврат'), ('magister', 'магістратура'), ('specialist', 'спеціалісти')], verbose_name='освітньо-кваліфікаційний рівень')),
                ('type', models.CharField(max_length=10, choices=[('daily', 'денна'), ('extramural', 'заочна')], verbose_name='форма навчання')),
            ],
            options={
                'verbose_name': 'група',
                'verbose_name_plural': 'групи',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupIndex',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('alias', models.CharField(max_length=8)),
                ('group', models.ForeignKey(to='core.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('week', models.PositiveSmallIntegerField(choices=[(1, 'перший'), (2, 'другий')], verbose_name='тиждень')),
                ('weekday', models.PositiveSmallIntegerField(choices=[(1, 'пн'), (2, 'вт'), (3, 'ср'), (4, 'чт'), (5, 'пт'), (6, 'сб'), (7, 'нд')], verbose_name='день')),
                ('number', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='пара')),
                ('place', models.CharField(max_length=10, null=True, verbose_name='аудиторія')),
                ('type', models.CharField(max_length=16, choices=[('lecture', 'лекція'), ('lab', 'лаба'), ('practice', 'практика')], null=True, verbose_name='тип заняття')),
                ('course', models.ForeignKey(to='core.Course', verbose_name='курс')),
                ('groups', models.ManyToManyField(to='core.Group', verbose_name='групи')),
            ],
            options={
                'verbose_name': 'заняття',
                'verbose_name_plural': 'заняття',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('first_week_monday', models.DateField()),
            ],
            options={
                'verbose_name': 'Налаштування сайту',
                'verbose_name_plural': 'Налаштування сайту',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
            field=models.ForeignKey(to='core.Teacher', verbose_name='викладач', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together=set([('course', 'week', 'weekday', 'number', 'place')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupindex',
            unique_together=set([('alias', 'group')]),
        ),
    ]
