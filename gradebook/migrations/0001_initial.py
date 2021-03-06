# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-08 15:46
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommonCoreStateStandard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('K', 'Kindergarten'), ('1st', '1st Grade'), ('2nd', '2nd Grade'), ('3rd', '3rd Grade'), ('4th', '4th Grade'), ('5th', '5th Grade'), ('6th', '6th Grade'), ('7th', '7th Grade'), ('8th', '8th Grade')], default='2nd', max_length=50)),
                ('domain', models.CharField(default='Reading', max_length=50)),
                ('subdomain', models.CharField(blank=True, max_length=100)),
                ('topic', models.CharField(default='Key Ideas and Details', max_length=100)),
                ('code', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^CCSS\\.(.*)$', 'Pattern must match IXL format: D-A.12')], verbose_name='CCSS Code')),
                ('description', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'Common Core Standards',
                'verbose_name': 'Common Core Standard',
            },
        ),
    ]
