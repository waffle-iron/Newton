# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 11:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0016_auto_20160801_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nwearitband',
            name='sub_domain',
        ),
        migrations.RemoveField(
            model_name='nweasubdomain',
            name='domain',
        ),
        migrations.DeleteModel(
            name='NWEATestResults',
        ),
        migrations.DeleteModel(
            name='NWEADomain',
        ),
        migrations.DeleteModel(
            name='NWEARITBand',
        ),
        migrations.DeleteModel(
            name='NWEASubDomain',
        ),
    ]
