# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-27 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nwea', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nweascore',
            name='year',
            field=models.CharField(choices=[('14-15', '14-15'), ('15-16', '15-16'), ('16-17', '16-17'), ('17-18', '17-18'), ('18-19', '18-19'), ('19-20', '19-20'), ('20-21', '20-21'), ('21-22', '21-22')], default='16-17', max_length=50),
        ),
    ]
