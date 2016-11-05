# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_exam'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthJournal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='\u0414\u0430\u0442\u0430')),
                ('present_day 0', models.BooleanField(default=False)),
                ('present_day 1', models.BooleanField(default=False)),
                ('present_day 2', models.BooleanField(default=False)),
                ('present_day 3', models.BooleanField(default=False)),
                ('present_day 4', models.BooleanField(default=False)),
                ('present_day 5', models.BooleanField(default=False)),
                ('present_day 6', models.BooleanField(default=False)),
                ('present_day 7', models.BooleanField(default=False)),
                ('present_day 8', models.BooleanField(default=False)),
                ('present_day 9', models.BooleanField(default=False)),
                ('present_day 10', models.BooleanField(default=False)),
                ('present_day 11', models.BooleanField(default=False)),
                ('present_day 12', models.BooleanField(default=False)),
                ('present_day 13', models.BooleanField(default=False)),
                ('present_day 14', models.BooleanField(default=False)),
                ('present_day 15', models.BooleanField(default=False)),
                ('present_day 16', models.BooleanField(default=False)),
                ('present_day 17', models.BooleanField(default=False)),
                ('present_day 18', models.BooleanField(default=False)),
                ('present_day 19', models.BooleanField(default=False)),
                ('present_day 20', models.BooleanField(default=False)),
                ('present_day 21', models.BooleanField(default=False)),
                ('present_day 22', models.BooleanField(default=False)),
                ('present_day 23', models.BooleanField(default=False)),
                ('present_day 24', models.BooleanField(default=False)),
                ('present_day 25', models.BooleanField(default=False)),
                ('present_day 26', models.BooleanField(default=False)),
                ('present_day 27', models.BooleanField(default=False)),
                ('present_day 28', models.BooleanField(default=False)),
                ('present_day 29', models.BooleanField(default=False)),
                ('present_day 30', models.BooleanField(default=False)),
                ('present_day 31', models.BooleanField(default=False)),
                ('student', models.ForeignKey(unique_for_month=b'date', verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442', to='students.Student')),
            ],
            options={
                'verbose_name': '\u041c\u0456\u0441\u044f\u0447\u043d\u0438\u0439 \u0416\u0443\u0440\u043d\u0430\u043b',
                'verbose_name_plural': '\u041c\u0456\u0441\u044f\u0447\u043d\u0456  \u0416\u0443\u0440\u043d\u0430\u043b\u0438',
            },
        ),
    ]
