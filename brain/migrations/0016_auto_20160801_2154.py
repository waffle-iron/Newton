# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 21:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0015_auto_20160801_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nweadomain',
            name='Domain',
        ),
        migrations.AddField(
            model_name='nweadomain',
            name='domain',
            field=models.IntegerField(choices=[(1, 'Operations and Algebraic Thinking'), (2, 'Number and Operations'), (3, 'Measurement and Data'), (4, 'Geometry')], default=1, verbose_name='Domain'),
        ),
    ]
