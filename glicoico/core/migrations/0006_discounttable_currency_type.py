# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-17 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20171210_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='discounttable',
            name='currency_type',
            field=models.IntegerField(choices=[(1, 'BTP'), (2, 'ETHER')], default=1),
        ),
    ]