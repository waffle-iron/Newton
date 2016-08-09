# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 21:54
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0014_auto_20160801_2041'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currentclass',
            options={'verbose_name': 'Class', 'verbose_name_plural': 'Classes'},
        ),
        migrations.RenameField(
            model_name='nweadomain',
            old_name='domain',
            new_name='Domain',
        ),
        migrations.AlterField(
            model_name='ixlskill',
            name='ixl_url',
            field=models.CharField(blank=True, max_length=300, verbose_name='IXL URL'),
        ),
        migrations.AlterField(
            model_name='ixlskill',
            name='skill_description',
            field=models.CharField(blank=True, max_length=200, verbose_name='Skill Description'),
        ),
        migrations.AlterField(
            model_name='ixlskill',
            name='skill_id',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator('^\\w\\-\\w\\.\\d+$', 'Pattern must match IXL format: D-A.12')], verbose_name='Skill ID'),
        ),
        migrations.AlterField(
            model_name='ixlskillscores',
            name='date_recorded',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Date Recorded'),
        ),
        migrations.AlterField(
            model_name='ixlskillscores',
            name='ixl_skill_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.IXLSkill', verbose_name='IXL Skill ID'),
        ),
        migrations.AlterField(
            model_name='nweasubdomain',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.NWEADomain', verbose_name='Domain'),
        ),
        migrations.AlterField(
            model_name='nweasubdomain',
            name='sub_domain',
            field=models.IntegerField(choices=[(1, 'Represent and Solve Problems'), (2, 'Properties of Operations'), (3, 'Understand Place Value, Counting, and Cardinality'), (4, 'Number and Operations: Base Ten and Fractions'), (5, 'Solve Problems Involving Measurement'), (6, 'Represent and Interpret Data'), (7, 'Reason with Shapes and Their Attributes')], default=1, verbose_name='Sub-Domain'),
        ),
    ]
