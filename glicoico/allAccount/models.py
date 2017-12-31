# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
TRANSACTION_TYPE = (
    ('pending', 'Pending'),
    ('successful', 'Successful'),
    ('failed', 'Failed'),
    ('cancelled', 'Cancelled'),
)

Address_Status = (
    ('initial', 'Initial'),
    ('assigned', 'Assigned'),
    ('used', 'Used'),
)


class SignUp(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    sponsered_id = models.CharField(max_length=100, null=True, blank=True)
    referal_code = models.CharField(max_length=10)
    referal_bonus = models.FloatField(null=True, blank=True)
    account_verified = models.BooleanField(default=False)
    btc_address = models.CharField(max_length=1000, null=True, blank=True, unique=True)
    eth_address = models.CharField(max_length=1000, null=True, blank=True, unique=True)
    verify_link = models.CharField(max_length=1000, null=True, blank=True, unique=True)
    pwd_verify_link = models.CharField(max_length=1000, null=True, blank=True, unique=True)

    def __unicode__(self):
        return self.user.username


class Transactions(models.Model):
    user = models.ForeignKey(SignUp)
    token = models.FloatField(null=True, blank=True)
    transaction_type = models.ManyToManyField('Coins')
    transaction_address_btc = models.ForeignKey('BitcoinAddress', null=True, blank=True)
    transaction_address_eth = models.ForeignKey('EtherumAddress', null=True, blank=True)
    value = models.FloatField()
    transaction_status = models.CharField(max_length=120, choices=TRANSACTION_TYPE, default='pending', blank=True,
                                          null=True)
    transaction_date = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)
    timestamp = models.DateField(auto_now_add=True, auto_now=False)
    bonus_process = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.user.username


class Coins(models.Model):
    name = models.CharField(max_length=120)
    token = models.PositiveIntegerField()
    value = models.FloatField()

    def __unicode__(self):
        return self.name


class BitcoinAddress(models.Model):
    address = models.CharField(max_length=500, unique=True)
    status = models.CharField(max_length=120, choices=Address_Status, default='initial')

    def __unicode__(self):
        return self.address


class EtherumAddress(models.Model):
    address = models.CharField(max_length=500, unique=True)
    status = models.CharField(max_length=120, choices=Address_Status, default='initial')

    def __unicode__(self):
        return self.address


class AssignedAddresses(models.Model):
    user = models.ForeignKey(SignUp)
    address = models.CharField(max_length=500)
    address_type = models.CharField(max_length=120, null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.user.username


class Subscription(models.Model):
    email = models.CharField(max_length=500)

    def __unicode__(self):
        return self.email

