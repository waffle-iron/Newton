# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-05 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ixl', '0017_auto_20161030_0110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challengeassignment',
            name='complete',
        ),
        migrations.AlterField(
            model_name='challenge',
            name='title',
            field=models.CharField(default='Challenge', max_length=250, unique=True, verbose_name='Challenge Title'),
        ),
    ]