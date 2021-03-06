# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-20 13:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0044_schedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200, verbose_name='Subject')),
            ],
        ),
        migrations.AlterField(
            model_name='schedule',
            name='subject1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject1', to='brain.Subject', verbose_name='First Class'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='subject2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject2', to='brain.Subject', verbose_name='Second Class'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='subject3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject3', to='brain.Subject', verbose_name='Third Class'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='subject4',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject4', to='brain.Subject', verbose_name='Fourth Class'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='subject5',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject5', to='brain.Subject', verbose_name='Fifth Class'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='subject6',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject6', to='brain.Subject', verbose_name='Sixth Class'),
        ),
    ]
