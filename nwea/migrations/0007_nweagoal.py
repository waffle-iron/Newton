# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-29 03:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0047_schedule_subject7'),
        ('nwea', '0006_nweaaverage'),
    ]

    operations = [
        migrations.CreateModel(
            name='NWEAGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('14-15', '14-15'), ('15-16', '15-16'), ('16-17', '16-17'), ('17-18', '17-18'), ('18-19', '18-19'), ('19-20', '19-20'), ('20-21', '20-21'), ('21-22', '21-22')], default='16-17', max_length=50)),
                ('math_winter', models.IntegerField()),
                ('math_spring', models.IntegerField()),
                ('reading_winter', models.IntegerField()),
                ('reading_spring', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.StudentRoster')),
            ],
        ),
    ]