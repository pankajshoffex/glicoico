# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import SignUp, Transactions, Coins, BitcoinAddress, EtherumAddress, AssignedAddresses, Subscription
from core.models import EtherScanTransaction
from core.views import (get_total_ether_bonus_per_user, get_total_ether_tokens_per_user, get_total_ether_per_user)


# Register your models here.

# class ProductImageInline(admin.TabularInline):
# 	model = Transactions
# 	fields = ('image', 'render_image',)
# 	readonly_fields = ('render_image',)
# 	extra = 0
# 	min_num = 1
# 	max_num = 4

class TransactionAdminInline(admin.TabularInline):
    model = Transactions
    extra = 0
# fields = ['transaction_type',
# 'token', 'transaction_address_btc', 'transaction_address_eth', 'value',
# 'transaction_status', 'transaction_date']


class AssignedAddressesAdminInline(admin.TabularInline):
    model = AssignedAddresses
    extra = 0


class SignUpAdmin(admin.ModelAdmin):
    inlines = [
        TransactionAdminInline,
        AssignedAddressesAdminInline,
    ]

    list_display = ['__unicode__', 'account_verified', 'referal_code',
                    'sponsered_id', 'eth_address', 'glc_points', 'total_ether', 'glc_bonus']
    search_fields = ['referal_code', 'btc_address', 'eth_address', 'user__username', 'sponsered_id']

    def glc_points(self, obj):
        return get_total_ether_tokens_per_user(obj.user)

    def total_ether(self, obj):
        return get_total_ether_per_user(obj.user)

    def glc_bonus(self, obj):
        return get_total_ether_bonus_per_user(obj.user)

    class Meta:
        model = SignUp


class AssignedAddressesAdmin(admin.ModelAdmin):
    search_fields = ['address']

    class Meta:
        model = AssignedAddresses


admin.site.register(Coins)
admin.site.register(SignUp, SignUpAdmin)
admin.site.register(Transactions)
admin.site.register(BitcoinAddress)
admin.site.register(EtherumAddress)
admin.site.register(AssignedAddresses, AssignedAddressesAdmin)
admin.site.register(Subscription)

