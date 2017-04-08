# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-04 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mathcgi', '0002_cgi_gr2_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='cgi',
            name='date_assigned',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cgi',
            name='first_num_original',
            field=models.IntegerField(null=True, verbose_name="Original Problem's First Number"),
        ),
        migrations.AddField(
            model_name='cgi',
            name='second_num_original',
            field=models.IntegerField(null=True, verbose_name="Original Problem's Second Number"),
        ),
        migrations.AlterField(
            model_name='cgi',
            name='first_num_high',
            field=models.IntegerField(verbose_name='Maximum for First Number'),
        ),
        migrations.AlterField(
            model_name='cgi',
            name='first_num_low',
            field=models.IntegerField(verbose_name='Minimum for First Number'),
        ),
        migrations.AlterField(
            model_name='cgi',
            name='gr2_unit',
            field=models.IntegerField(help_text='The Unit in the Grade 2 Scope and Sequence which the CGI is introduced', verbose_name='Grade 2 Unit'),
        ),
        migrations.AlterField(
            model_name='cgi',
            name='second_num_high',
            field=models.IntegerField(verbose_name='Maximum for Second Number'),
        ),
        migrations.AlterField(
            model_name='cgi',
            name='second_num_low',
            field=models.IntegerField(verbose_name='Minimum for Second Number'),
        ),
    ]
