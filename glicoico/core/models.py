# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class NotifyEmail(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return self.name


class TokenSale(models.Model):
    pre_sale = models.PositiveIntegerField(default=0, null=True, blank=True)
    ico = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return str(self.ico)


class Invoice(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    invoice_id = models.BigIntegerField(unique=True)
    address = models.TextField(verbose_name='btc_address', blank=True)
    callback_url = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.invoice_id)


class InvoicePayment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    transaction_hash = models.TextField()
    value = models.FloatField(default=0.00)
    is_old_adress = models.BooleanField(default=False)
    created = models.DateTimeField(default=datetime.now, blank=True)
    btp_rate = models.FloatField(default=112533)
    bonus_percent = models.FloatField(default=15)

    def __unicode__(self):
        return str(self.invoice.invoice_id)


class PendingInvoicePayment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    transaction_hash = models.TextField()
    value = models.FloatField(default=0.00)

    def __unicode__(self):
        return str(self.invoice.invoice_id)


class EtherScanTransaction(models.Model):
    blockNumber = models.TextField(blank=True)
    timeStamp = models.TextField(blank=True)
    hash = models.TextField(blank=True)
    nonce = models.TextField(blank=True)
    blockHash = models.TextField(blank=True)
    transactionIndex = models.TextField(blank=True)
    e_from = models.TextField(blank=True)
    e_to = models.TextField(blank=True)
    value = models.TextField(blank=True)
    gas = models.TextField(blank=True)
    gasPrice = models.TextField(blank=True)
    isError = models.TextField(blank=True)
    txreceipt_status = models.TextField(blank=True)
    input = models.TextField(blank=True)
    contractAddress = models.TextField(blank=True)
    cumulativeGasUsed = models.TextField(blank=True)
    gasUsed = models.TextField(blank=True)
    confirmations = models.TextField(blank=True)
    btp_rate = models.FloatField(default=5166)
    bonus_percent = models.FloatField(default=15)

    def __unicode__(self):
        return self.e_from


class DiscountTable(models.Model):
    CURRENCY_TYPE = (
        (1, 'BTP'),
        (2, 'ETHER')
        )
    title = models.CharField(max_length=120, blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    btp_rate = models.FloatField()
    currency_type = models.IntegerField(default=1, choices=CURRENCY_TYPE)

    def __unicode__(self):
        return str(self.btp_rate)


class BonusTable(models.Model):
    title = models.CharField(max_length=120, blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    percentage = models.FloatField()

    def __unicode__(self):
        return str(self.percentage)


