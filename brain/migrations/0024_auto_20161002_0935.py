# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-02 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0023_accountinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountinfo',
            name='kidsazteacher',
            field=models.CharField(blank=True, max_length=200, verbose_name='Kids A-Z Teacher'),
        ),
    ]
