# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-24 03:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brain', '0047_schedule_subject7'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_selected', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Sticker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='stickers')),
            ],
        ),
        migrations.CreateModel(
            name='StickerAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earned', models.BooleanField(default=True)),
                ('sticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='badges.Sticker')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.StudentRoster')),
            ],
        ),
        migrations.AddField(
            model_name='avatar',
            name='sticker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='badges.Sticker'),
        ),
        migrations.AddField(
            model_name='avatar',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.StudentRoster'),
        ),
    ]
