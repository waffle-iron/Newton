# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-26 21:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreit', '0004_auto_20161126_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]
