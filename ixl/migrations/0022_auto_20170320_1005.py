# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-20 10:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ixl', '0021_challengeexercise_required_score'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='challenge',
            options={'ordering': ['-date', 'title'], 'verbose_name': 'IXL Challenge', 'verbose_name_plural': 'IXL Challenges'},
        ),
    ]
