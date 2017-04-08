# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-24 00:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scoreit', '0002_auto_20161121_0126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='criteria',
            options={'ordering': ['ordering'], 'verbose_name': 'Criteria', 'verbose_name_plural': 'Criteria'},
        ),
        migrations.AlterModelOptions(
            name='criteriascore',
            options={'ordering': ['criteria__ordering'], 'verbose_name': 'Criteria Score', 'verbose_name_plural': 'Criteria Scores'},
        ),
        migrations.RemoveField(
            model_name='criteriascore',
            name='subject',
        ),
    ]
