# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-23 11:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import web_api.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.PositiveSmallIntegerField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('place_id', models.CharField(default='null_id', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=40)),
                ('latitude', models.DecimalField(decimal_places=10, max_digits=15)),
                ('longitude', models.DecimalField(decimal_places=10, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=datetime.date.today)),
                ('total_logins', models.IntegerField()),
                ('total_matches', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('imei', models.CharField(max_length=16, primary_key=True, serialize=False, unique=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'None')], max_length=1)),
                ('time_of_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=web_api.models.selfie_directory)),
                ('imei_hash', models.CharField(default='default_hash', max_length=255)),
                ('is_authenticated', models.BooleanField(default=False)),
                ('fcm_id', models.CharField(blank=True, max_length=255, null=True)),
                ('login_time', models.IntegerField(blank=True, default=0)),
                ('last_check', models.IntegerField(blank=True, default=0)),
                ('liked_users', models.ManyToManyField(blank=True, related_name='selected_users', to='web_api.User')),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='current_users',
            field=models.ManyToManyField(blank=True, to='web_api.User'),
        ),
        migrations.AddField(
            model_name='message',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='web_api.User'),
        ),
        migrations.AddField(
            model_name='message',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='web_api.User'),
        ),
    ]
