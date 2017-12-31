# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-10 13:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_etherscantransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='BonusTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=120)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('percentage', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DiscountTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=120)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('btp_rate', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='etherscantransaction',
            name='bonus_percent',
            field=models.FloatField(default=15),
        ),
        migrations.AddField(
            model_name='etherscantransaction',
            name='btp_rate',
            field=models.FloatField(default=5166),
        ),
        migrations.AddField(
            model_name='invoicepayment',
            name='bonus_percent',
            field=models.FloatField(default=15),
        ),
        migrations.AddField(
            model_name='invoicepayment',
            name='btp_rate',
            field=models.FloatField(default=112533),
        ),
        migrations.AddField(
            model_name='invoicepayment',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
