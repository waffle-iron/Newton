# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0012_auto_20160801_2005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='teacher',
            new_name='last_name',
        ),
        migrations.AddField(
            model_name='teacher',
            name='first_name',
            field=models.CharField(default='Alex', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='title',
            field=models.CharField(choices=[('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'), ('Mr.', 'Mr.'), ('Dr.', 'Dr.')], default='Ms.', max_length=50),
        ),
    ]
