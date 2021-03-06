# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-30 01:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ixl', '0016_auto_20161009_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengeExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterModelOptions(
            name='challengeassignment',
            options={'ordering': ['date_assigned', 'challenge', 'student_id'], 'verbose_name': 'IXL Challenge Assignment', 'verbose_name_plural': 'IXL Challenge Assignments'},
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise1',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise10',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise11',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise12',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise13',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise14',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise15',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise2',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise3',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise4',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise5',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise6',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise7',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise8',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='exercise9',
        ),
        migrations.AddField(
            model_name='challengeexercise',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ixl.Challenge'),
        ),
    ]
