# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-05 20:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0019_auto_20160804_2117'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NWEAIXLMatch',
        ),
        migrations.AlterModelOptions(
            name='currentclass',
            options={'ordering': ['year', 'grade', 'teacher'], 'verbose_name': 'Class', 'verbose_name_plural': 'Classes'},
        ),
        migrations.AlterModelOptions(
            name='studentroster',
            options={'ordering': ['current_class', 'last_name'], 'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['last_name'], 'verbose_name': 'Teacher', 'verbose_name_plural': 'Teachers'},
        ),
    ]
