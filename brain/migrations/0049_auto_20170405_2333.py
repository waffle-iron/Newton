# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-05 23:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0048_dataupdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataupdate',
            name='dateandtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 5, 19, 33, 19, 637822, tzinfo=utc)),
        ),
    ]
