# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 00:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0003_auto_20160725_0021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentroster',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='studentroster',
            name='email',
        ),
        migrations.RemoveField(
            model_name='studentroster',
            name='gender',
        ),
    ]
