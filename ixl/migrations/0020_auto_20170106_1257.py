# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-06 12:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ixl', '0019_remove_challengeassignment_current_challenge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='challengeassignment',
            options={'ordering': ['-date_assigned', 'challenge', 'student_id'], 'verbose_name': 'IXL Challenge Assignment', 'verbose_name_plural': 'IXL Challenge Assignments'},
        ),
    ]
