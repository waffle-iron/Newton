# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-06 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mathcgi', '0007_auto_20161105_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cgi',
            name='question',
            field=models.TextField(help_text='Substitute __ for the numbers in the problem.', max_length=500, unique=True, verbose_name='Problem'),
        ),
    ]
