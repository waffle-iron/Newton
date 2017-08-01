# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-20 13:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0043_auto_20161113_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('MONDAY', 'Monday'), ('TUESDAY', 'Tuesday'), ('WEDNESDAY', 'Wednesday'), ('THURSDAY', 'Thursday'), ('FRIDAY', 'Friday')], max_length=200)),
                ('subject1', models.CharField(choices=[('Reading', 'Reading'), ('Writing', 'Writing'), ('Math', 'Math'), ('Core Knowledge', 'Core Knowledge'), ('Science', 'Science'), ('Art', 'Art'), ('Spanish', 'Spanish'), ('Gym', 'Gym'), ('Dance', 'Dance')], max_length=200, verbose_name='First Class')),
                ('subject2', models.CharField(choices=[('Reading', 'Reading'), ('Writing', 'Writing'), ('Math', 'Math'), ('Core Knowledge', 'Core Knowledge'), ('Science', 'Science'), ('Art', 'Art'), ('Spanish', 'Spanish'), ('Gym', 'Gym'), ('Dance', 'Dance')], max_length=200, verbose_name='Second Class')),
                ('subject3', models.CharField(choices=[('Reading', 'Reading'), ('Writing', 'Writing'), ('Math', 'Math'), ('Core Knowledge', 'Core Knowledge'), ('Science', 'Science'), ('Art', 'Art'), ('Spanish', 'Spanish'), ('Gym', 'Gym'), ('Dance', 'Dance')], max_length=200, verbose_name='Third Class')),
                ('subject4', models.CharField(choices=[('Reading', 'Reading'), ('Writing', 'Writing'), ('Math', 'Math'), ('Core Knowledge', 'Core Knowledge'), ('Science', 'Science'), ('Art', 'Art'), ('Spanish', 'Spanish'), ('Gym', 'Gym'), ('Dance', 'Dance')], max_length=200, verbose_name='Fourth Class')),
                ('subject5', models.CharField(choices=[('Reading', 'Reading'), ('Writing', 'Writing'), ('Math', 'Math'), ('Core Knowledge', 'Core Knowledge'), ('Science', 'Science'), ('Art', 'Art'), ('Spanish', 'Spanish'), ('Gym', 'Gym'), ('Dance', 'Dance')], max_length=200, verbose_name='Fifth Class')),
                ('subject6', models.CharField(choices=[('Reading', 'Reading'), ('Writing', 'Writing'), ('Math', 'Math'), ('Core Knowledge', 'Core Knowledge'), ('Science', 'Science'), ('Art', 'Art'), ('Spanish', 'Spanish'), ('Gym', 'Gym'), ('Dance', 'Dance')], max_length=200, verbose_name='Sixth Class')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.Teacher')),
            ],
        ),
    ]