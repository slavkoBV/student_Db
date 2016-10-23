# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='ticket',
            field=models.IntegerField(max_length=256, verbose_name='\u0411\u0456\u043b\u0435\u0442'),
        ),
    ]
