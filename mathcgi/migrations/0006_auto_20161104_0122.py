# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-04 01:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mathcgi', '0005_auto_20161104_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cgi',
            name='gr2_unit',
            field=models.IntegerField(blank=True, help_text='The Unit in the Grade 2 Scope and Sequence which the CGI is introduced', null=True, verbose_name='Grade 2 Unit'),
        ),
    ]
