# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 16:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedAddresses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500)),
                ('address_type', models.CharField(blank=True, max_length=120, null=True)),
                ('is_used', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BitcoinAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500, unique=True)),
                ('status', models.CharField(choices=[('initial', 'Initial'), ('assigned', 'Assigned'), ('used', 'Used')], default='initial', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Coins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('token', models.PositiveIntegerField()),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='EtherumAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500, unique=True)),
                ('status', models.CharField(choices=[('initial', 'Initial'), ('assigned', 'Assigned'), ('used', 'Used')], default='initial', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('sponsered_id', models.CharField(blank=True, max_length=100, null=True)),
                ('referal_code', models.CharField(max_length=10)),
                ('referal_bonus', models.FloatField(blank=True, null=True)),
                ('account_verified', models.BooleanField(default=False)),
                ('btc_address', models.CharField(blank=True, max_length=1000, null=True, unique=True)),
                ('eth_address', models.CharField(blank=True, max_length=1000, null=True, unique=True)),
                ('verify_link', models.CharField(blank=True, max_length=1000, null=True, unique=True)),
                ('pwd_verify_link', models.CharField(blank=True, max_length=1000, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.FloatField(blank=True, null=True)),
                ('value', models.FloatField()),
                ('transaction_status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed'), ('cancelled', 'Cancelled')], default='pending', max_length=120, null=True)),
                ('transaction_date', models.DateField(blank=True, null=True)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('bonus_process', models.BooleanField(default=False)),
                ('transaction_address_btc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='allAccount.BitcoinAddress')),
                ('transaction_address_eth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='allAccount.EtherumAddress')),
                ('transaction_type', models.ManyToManyField(to='allAccount.Coins')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allAccount.SignUp')),
            ],
        ),
        migrations.AddField(
            model_name='assignedaddresses',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allAccount.SignUp'),
        ),
    ]
