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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('prefix', models.CharField(max_length=4, verbose_name='префікс')),
                ('code', models.CharField(max_length=8, unique=True, verbose_name='шифр')),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=16, choices=[('lecture', 'лекція'), ('lab', 'лаба'), ('practice', 'практика')])),
                ('week', models.PositiveSmallIntegerField(verbose_name='тиждень', choices=[(1, 'перший'), (2, 'другий')])),
                ('weekday', models.PositiveSmallIntegerField(verbose_name='день', choices=[(1, 'пн'), (2, 'вт'), (3, 'ср'), (4, 'чт'), (5, 'пт'), (6, 'сб'), (7, 'нд')])),
                ('number', models.PositiveSmallIntegerField(verbose_name='пара', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('course', models.ForeignKey(to='core.Course', verbose_name='курс')),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
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
            unique_together=set([('group', 'short_name'), ('group', 'full_name')]),
        ),
    ]
