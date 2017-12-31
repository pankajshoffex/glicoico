import os
import sys
import django
import json
import time
import datetime

the_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(the_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BitPaid.settings")
django.setup()

from core.models import EtherScanTransaction, DiscountTable, BonusTable
from core.ether_account import Account

ADDRESS = "0x0742D21b67DC40fe6Ad6d82D518392F6697bFb80"
ETHER_API_KEY = "38908c038bf049d3b9a75984313d406a"


def get_ether_data():
    try:
        acc = Account(address=ADDRESS, api_key=ETHER_API_KEY)
        data = acc.get_all_transactions()
        if data:
            ether_scan_list = EtherScanTransaction.objects.all()
            if len(data) > ether_scan_list.count():
                actual_list = data[ether_scan_list.count():]
                for obj in actual_list:
                    try:
                        eth_obj = EtherScanTransaction.objects.create(
                            blockNumber=obj['blockNumber'],
                            timeStamp=obj['timeStamp'],
                            hash=obj['hash'],
                            nonce=obj['nonce'],
                            blockHash=obj['blockHash'],
                            transactionIndex=obj['transactionIndex'],
                            e_from=obj['from'],
                            e_to=obj['to'],
                            value=obj['value'],
                            gas=obj['gas'],
                            gasPrice=obj['gasPrice'],
                            isError=obj['isError'],
                            txreceipt_status=obj['txreceipt_status'],
                            input=obj['input'],
                            contractAddress=obj['contractAddress'],
                            cumulativeGasUsed=obj['cumulativeGasUsed'],
                            gasUsed=obj['gasUsed'],
                            confirmations=obj['confirmations']
                        )
                        today = datetime.datetime.now().date()
                        discount_obj = DiscountTable.objects.filter(
                            from_date__lte=today, 
                            to_date__gte=today,
                            currency_type=2
                            ).first()
                        if discount_obj:
                            eth_obj.btp_rate = discount_obj.btp_rate
                            eth_obj.save()

                        bonus_obj = BonusTable.objects.filter(from_date__lte=today, to_date__gte=today).first()
                        if bonus_obj:
                            eth_obj.bonus_percent = bonus_obj.percentage
                            eth_obj.save()
                    except Exception as e:
                        print(e)
    except Exception as f:
        print(f)


if __name__ == '__main__':
    while True:
        get_ether_data()
        time.sleep(600)

