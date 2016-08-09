# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 12:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0008_auto_20160725_1151'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currentclass',
            options={'verbose_name': 'Current Class', 'verbose_name_plural': 'Current Classes'},
        ),
        migrations.AlterModelOptions(
            name='ixlskill',
            options={'verbose_name': 'IXL Skill', 'verbose_name_plural': 'IXL Skills '},
        ),
        migrations.AlterModelOptions(
            name='ixlskillscores',
            options={'verbose_name': 'IXL Skill Score', 'verbose_name_plural': 'IXL Skill Scores'},
        ),
        migrations.AlterModelOptions(
            name='studentroster',
            options={'verbose_name': 'Student Roster', 'verbose_name_plural': 'Student Rosters'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': 'Teacher', 'verbose_name_plural': 'Teachers'},
        ),
    ]
