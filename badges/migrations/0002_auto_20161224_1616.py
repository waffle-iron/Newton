# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-24 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sticker',
            name='image',
            field=models.FilePathField(verbose_name='static/images'),
        ),
    ]
