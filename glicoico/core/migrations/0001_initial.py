# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-11 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TokenSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pre_sale', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('ico', models.PositiveIntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]
