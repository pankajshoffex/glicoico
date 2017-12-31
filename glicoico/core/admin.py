# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import (
    NotifyEmail, TokenSale, Invoice,
    InvoicePayment, PendingInvoicePayment, EtherScanTransaction, DiscountTable, BonusTable)
from .views import (
    get_total_tokens_per_user, get_total_bonus_per_user,
    get_total_ether_bonus_per_user, get_total_ether_tokens_per_user, get_total_btc_per_user)


class InvoicePaymentAdminInline(admin.TabularInline):
    model = InvoicePayment
    extra = 0
    verbose_name = "Confirmed Payment"
    verbose_name_plural = "Confirmed Payments"


class PendingInvoicePaymentAdminInline(admin.TabularInline):
    model = PendingInvoicePayment
    extra = 0
    verbose_name = "Pending Payment"
    verbose_name_plural = "Pending Payments"


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [
        InvoicePaymentAdminInline,
        PendingInvoicePaymentAdminInline,
    ]

    list_display = ['invoice_id', 'address', 'user', 'total_btp', 'total_btc', 'total_bonus_btp']

    def total_btp(self, obj):
        return get_total_tokens_per_user(obj.user)

    def total_btc(self, obj):
        return get_total_btc_per_user(obj.user)

    def total_bonus_btp(self, obj):
        return get_total_bonus_per_user(obj.user)

    class Meta:
        model = Invoice


class EtherScanTransactionAdmin(admin.ModelAdmin):
    list_display = ['e_from', 'e_to', 'hash']

    class Meta:
        model = EtherScanTransaction


class DiscountTableAdmin(admin.ModelAdmin):
    list_display = ['currency_type', 'from_date', "to_date", 'btp_rate', 'title']

    class Meta:
        model = DiscountTable


class BonusTableAdmin(admin.ModelAdmin):
    list_display = ['from_date', "to_date", 'percentage', 'title']

    class Meta:
        model = BonusTable


admin.site.register(NotifyEmail)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(EtherScanTransaction, EtherScanTransactionAdmin)
admin.site.register(DiscountTable, DiscountTableAdmin)
admin.site.register(BonusTable, BonusTableAdmin)
admin.site.register(TokenSale)

