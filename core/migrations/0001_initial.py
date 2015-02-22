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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('short_name', models.CharField(verbose_name='коротка назва', max_length=8)),
                ('full_name', models.CharField(verbose_name='повна назва', max_length=128)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('prefix', models.CharField(verbose_name='префікс', max_length=4)),
                ('code', models.CharField(unique=True, verbose_name='шифр', max_length=8)),
                ('okr', models.CharField(choices=[('bachelor', 'бакалаврат'), ('magister', 'магістратура'), ('specialist', 'спеціалісти')], verbose_name='освітньо-кваліфікаційний рівень', max_length=16)),
                ('type', models.CharField(choices=[('daily', 'денна'), ('extramural', 'заочна')], verbose_name='форма навчання', max_length=10)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('type', models.CharField(choices=[('lecture', 'лекція'), ('lab', 'лаба'), ('practice', 'практика')], verbose_name='тип заняття', max_length=16)),
                ('place', models.CharField(verbose_name='місце проведення', max_length=10)),
                ('week', models.PositiveSmallIntegerField(verbose_name='тиждень', choices=[(1, 'перший'), (2, 'другий')])),
                ('weekday', models.PositiveSmallIntegerField(verbose_name='день', choices=[(1, 'пн'), (2, 'вт'), (3, 'ср'), (4, 'чт'), (5, 'пт'), (6, 'сб'), (7, 'нд')])),
                ('number', models.PositiveSmallIntegerField(verbose_name='пара', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('course', models.ForeignKey(to='core.Course', verbose_name='курс')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
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
            field=models.ForeignKey(null=True, verbose_name='викладач', to='core.Teacher'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together=set([('course', 'week', 'weekday', 'number')]),
        ),
        migrations.AddField(
            model_name='course',
            name='group',
            field=models.ForeignKey(to='core.Group', verbose_name='група'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('group', 'full_name'), ('group', 'short_name')]),
        ),
    ]
