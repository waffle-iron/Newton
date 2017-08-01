# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-20 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20161113_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='subject',
            field=models.CharField(choices=[('WRITING', 'Writing'), ('READING', 'Reading'), ('MATH', 'Math'), ('CORE', 'Core Knowledge')], default='MATH', max_length=256, verbose_name='Subject'),
        ),
    ]