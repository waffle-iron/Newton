# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-08 15:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0049_auto_20170405_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataupdate',
            name='dateandtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 8, 11, 46, 34, 776167, tzinfo=utc)),
        ),
    ]