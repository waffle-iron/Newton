# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 00:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0002_auto_20160725_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ixlskillscores',
            name='score',
            field=models.IntegerField(),
        ),
    ]
