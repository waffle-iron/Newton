# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-06 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0029_readingstats_myon_time_spent'),
    ]

    operations = [
        migrations.AddField(
            model_name='readingstats',
            name='starting_lexile',
            field=models.IntegerField(blank=True, null=True, verbose_name='Starting Lexile Level'),
        ),
    ]
