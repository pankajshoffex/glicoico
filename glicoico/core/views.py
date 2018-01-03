# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.db.models import Sum

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.crypto import get_random_string

from allAccount.models import (SignUp, Subscription, BitcoinAddress, EtherumAddress, Transactions, AssignedAddresses)
from django.core.mail import EmailMessage, EmailMultiAlternatives
import random
from blockchain.v2.receive import receive
import datetime

from .models import (
    NotifyEmail, TokenSale, Invoice,
    InvoicePayment, PendingInvoicePayment, EtherScanTransaction,
    DiscountTable, BonusTable
)


def get_todays_value(value):
    rate = None
    today = datetime.datetime.now().date()
    discount_obj = DiscountTable.objects.filter(
        from_date__lte=today, 
        to_date__gte=today,
        currency_type=value
    ).first()
    if discount_obj:
        rate = discount_obj.btp_rate

    return rate


def HomePage(request):
    context = {}

    sale = TokenSale.objects.all()
    for s in sale:
        context['pre'] = s.pre_sale
        context['ico'] = s.ico

    context['eth_rate'] = 3072
    eth_rate = get_todays_value(2)
    if eth_rate:
        context['eth_rate'] = eth_rate

    context['btc_rate'] = 53000
    btc_rate = get_todays_value(1)
    if btc_rate:
        context['btc_rate'] = btc_rate

    if request.method == 'POST':
        email = request.POST.get('email')
        chk_mail = Subscription.objects.filter(email=email)
        if email and not chk_mail:
            sub = Subscription()
            sub.email = email
            sub.save()
            context['mail'] = True
        else:
            context['fail'] = True

    return render(request, "index.html", context)


def login_in_account(request):
    context = {}
    try:
        try:
            current_user = User.objects.get(username=request.user)
            signup_user = SignUp.objects.get(user=current_user)
            if current_user and signup_user:
                context['login'] = True
                return HttpResponseRedirect('/account')
        except:
            pass
        if request.method == 'POST':
            username = request.POST.get("email")
            username = username.lower()
            password = request.POST.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/account')
                else:
                    return HttpResponseRedirect('/login')
            else:
                context['error'] = True

    except Exception as e:
        context['error'] = True

    return render(request, 'login1.html', context)


def signup(request, *args, **kwargs):
    try:
        context = {}
        if request.method == 'GET':
            ref_code = str(request.path).split("/")
            if len(ref_code) == 3:
                code = ref_code[-1]
                context['code'] = code
        counter = 1
        if request.method == 'POST':
            email = request.POST.get("email")
            email = email.lower()
            password = request.POST.get("password")
            sponser_id = request.POST.get("refral")

            # User object created
            new_user = User.objects.create_user(username=email)
            new_user.set_password(password)
            new_user.save()

            while True:
                refral_code = random.randint(100000, 999999)
                code = 'GLC' + str(refral_code)

                present = SignUp.objects.filter(referal_code=code).count()
                if present > 0:
                    pass
                else:
                    break

            random_str = get_random_string(length=32)
            # Signup object create
            signup_user = SignUp()
            signup_user.user = new_user
            signup_user.sponsered_id = sponser_id
            signup_user.referal_code = code
            signup_user.referal_bonus = 0
            signup_user.verify_link = random_str
            signup_user.save()
            try:
                subject, from_email, to = 'GLICO Account Verification.', 'support@glico.io', email
                text_content = 'GLICO Account verification Mail.'
                html_content = """<!DOCTYPE html>
								<html>
								<head>
									<title></title>
									<style type="text/css">
										.top-body{
											height: 180px;
											width: 100%;
											background-color: #19928c;
										}

										.main-panel{
											height: auto;
											width: 100%;
										}

										.main-body{
											background-color: white;
											font-size: 20px;
										}

										.verify-button{
											background-color: white;
											color: #19928c;
											border-color: #19928c;
											margin-left: 20%;
											height: 50px;
											width: 150px;
											font-size: 20px;
											cursor:pointer;
										}

										.disclaimer{
											font-size: 13px;
											color: gray;
										}

										body{
											line-height: 1.8em;
										}

										.main-panel{
											width: 100%;
											display: block;
											margin: auto;
											border:2px solid #2a928b;
											padding: 1%;
										}

										.email{
											color: #2a928b;
											font-size: 17px;
										}

										.logo{
											height: 100px;
											display: block;
											margin: auto;
										}

										.title{
											text-align: center;
											margin-top: -25px;
											font-size: 30px;
											color: white;
											padding-bottom: 10px;
										}
									</style>
								</head>
								<body>
								<div class="main-panel">
									<div class="top-body">
										
										<p class="title">GLICO</p>
									</div>
									<div class="main-body">
										
										<br><br>
										Dear <u>""" + str(email) + """,</u><br><br>
										&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We are happy to see you joining GLICO..!<br>
										To activate your wallet, please confirm your email address by clicking Verify Email:<br><br>
										<a href="http://glico.io/verify/""" + random_str + """"><button class="verify-button">Verify Email</button></a>
										<br><br>
										Or clicking the following link:<br>
										<span class="email">http://glico.io/verify/""" + random_str + """</span><br><br><br>
										<p>
											Get 40% Pre-sale GLC Bonus on your Referral<br>
											Link:- <b>http://glico.io/signup/""" + str(code) + """</b>
											<br><br>
											OR<br><br>
											Referral Code:- <b>""" + str(code) + """</b>

										</p>
										<p class="disclaimer">PLEASE DO NOT REPLY to this message. This email message was sent from a notification-only address that cannot accept incoming email. You received this email because you registered and accepted an invitation.

										If you have any questions, please feel free to to ask for help. Our support team will be able to help you through email support@glico.io.

										Sincerely, 
										GLICO team</p>
									</div>
								</div>
								</body>
								</html>"""
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except Exception as E:
                pass

            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/account')
                else:
                    return HttpResponseRedirect('/login')

    except Exception as e:
        context['old_acc'] = True
        # already exist account giv response
        print e

    return render(request, 'create_account.html', context)


@login_required(login_url='/login')
def GetUserAddress(request):
    context = {}
    invoice = Invoice.objects.filter(user=request.user).first()
    if invoice:
        context['btc_addr'] = invoice.address
        if invoice.address.replace(" ", "") == '17KeeBsPVbz83CtbA17KJQamMVSUq1un5X':
            callback_url = "http://www.glico.io/payment/" + str(
                invoice.invoice_id) + "/?secret=" + settings.PRIVATE_URL_KEY
            recv = receive(settings.XPUB, callback_url, settings.BLOCK_CHAIN_API_KEY)
            invoice.address = recv.address
            invoice.callback_url = callback_url
            invoice.save()
            context['btc_addr'] = invoice.address
    else:
        invoice_count = Invoice.objects.all().count()
        inv_id = 10001 + invoice_count
        invoice = Invoice.objects.create(
            user=request.user, invoice_id=inv_id)
        callback_url = "http://www.glico.io/payment/" + str(inv_id) + "/?secret=" + settings.PRIVATE_URL_KEY
        try:
            recv = receive(settings.XPUB, callback_url, settings.BLOCK_CHAIN_API_KEY)
            invoice.address = recv.address
            invoice.callback_url = callback_url
            invoice.save()
        except Exception as e:
            print e.message
            invoice.delete()
        context['btc_addr'] = invoice.address
    context['addrGet'] = True
    return render(request, 'get_address.html', context)


@user_passes_test(lambda u: u.is_superuser)
def calculator(request):
    return render(request, 'calcy.html', {})


def ComingSoon(request):
    try:
        context = {}

        if request.method == "POST":
            name = request.POST.get("email")
            if name:
                val = NotifyEmail.objects.filter(name=name).exists()
                if val != True:
                    notiy = NotifyEmail()
                    notiy.name = name
                    notiy.save()
                    context["submit"] = True
                else:
                    context["submit"] = False


    except:
        pass
    return render(request, "coming_soon.html", context)


BTP_RATE = 53000
ETHER_BTP_RATE = 3072


def get_total_tokens_per_user(user):
    tokens = 0.00
    invoiceObj = Invoice.objects.filter(user=user).first()
    if invoiceObj:
        confirm_invoices = InvoicePayment.objects.filter(invoice=invoiceObj).values(
            'transaction_hash', 'value', 'btp_rate')
        if confirm_invoices:
            temp_trans_list = []
            total_value = 0
            for obj in confirm_invoices:
                if obj['transaction_hash'] not in temp_trans_list:
                    temp_trans_list.append(obj['transaction_hash'])
                    temp_value = obj['value'] * obj['btp_rate']
                    total_value = total_value + temp_value

            tokens = total_value
    return tokens


def get_total_btc_per_user(user):
    tokens = 0.00
    invoiceObj = Invoice.objects.filter(user=user).first()
    if invoiceObj:
        confirm_invoices = InvoicePayment.objects.filter(invoice=invoiceObj).values(
            'transaction_hash', 'value')
        if confirm_invoices:
            temp_trans_list = []
            total_value = 0
            for obj in confirm_invoices:
                if obj['transaction_hash'] not in temp_trans_list:
                    temp_trans_list.append(obj['transaction_hash'])
                    total_value = total_value + obj['value']

            tokens = total_value
    return tokens


def get_total_ether_tokens_per_user(user):
    tokens = 0.00
    usereObj = SignUp.objects.filter(user=user).first()
    if usereObj:
        if usereObj.eth_address:
            if len(usereObj.eth_address) == 42:
                my_add = ""
                ether_data = EtherScanTransaction.objects.filter(
                    e_from__iexact=usereObj.eth_address,
                    e_to__iexact=my_add
                )
                wei_value = 0
                temp_trans_list = []
                for eth in ether_data:
                    if eth.hash not in temp_trans_list:
                        temp_trans_list.append(eth.hash)
                        ether_val = (float(eth.value) / float(1000000000000000000)) * float(eth.btp_rate)
                        wei_value += ether_val
                tokens = wei_value
    return tokens


def get_total_ether_per_user(user):
    tokens = 0.00
    usereObj = SignUp.objects.filter(user=user).first()
    if usereObj:
        if usereObj.eth_address:
            if len(usereObj.eth_address) == 42:
                my_add = ""
                ether_data = EtherScanTransaction.objects.filter(
                    e_from__iexact=usereObj.eth_address,
                    e_to__iexact=my_add
                )
                wei_value = 0
                temp_trans_list = []
                for eth in ether_data:
                    if eth.hash not in temp_trans_list:
                        temp_trans_list.append(eth.hash)
                        wei_value += float(eth.value)
                ether_val = float(wei_value) / float(1000000000000000000)
                tokens = ether_val
    return tokens


def get_total_bonus_per_user(user):
    signup_user = SignUp.objects.filter(user=user).first()
    referal_users = SignUp.objects.filter(sponsered_id=signup_user.referal_code)
    total_referal_amount = 0.00
    if referal_users:
        for ref_user in referal_users:
            invoiceObj = Invoice.objects.filter(user=ref_user.user).first()
            if invoiceObj:
                confirm_invoices = InvoicePayment.objects.filter(invoice=invoiceObj).values(
                    'transaction_hash', 'value', 'btp_rate', 'bonus_percent')
                if confirm_invoices:
                    temp_trans_list = []
                    total_value = 0
                    for obj in confirm_invoices:
                        if obj['transaction_hash'] not in temp_trans_list:
                            temp_trans_list.append(obj['transaction_hash'])
                            temp_value = obj['value'] * obj['btp_rate']
                            bonus_value = (temp_value * obj['bonus_percent']) / 100
                            total_value = total_value + bonus_value
                            total_referal_amount = total_referal_amount + total_value

    return total_referal_amount


def get_total_ether_bonus_per_user(user):
    signup_user = SignUp.objects.filter(user=user).first()
    referal_users = SignUp.objects.filter(sponsered_id=signup_user.referal_code)
    total_referal_amount = 0.00
    if referal_users:
        for ref_user in referal_users:
            usereObj = SignUp.objects.filter(user=ref_user.user).first()
            if usereObj:
                if usereObj.eth_address:
                    if len(usereObj.eth_address) == 42:
                        my_add = ""
                        ether_data = EtherScanTransaction.objects.filter(
                            e_from__iexact=usereObj.eth_address,
                            e_to__iexact=my_add
                        )
                        temp_trans_list = []
                        for eth in ether_data:
                            if eth.hash not in temp_trans_list:
                                temp_trans_list.append(eth.hash)
                                ether_val = (float(eth.value) / float(1000000000000000000)) * float(eth.btp_rate)
                                wei_value = (ether_val * float(eth.bonus_percent)) / 100
                                total_referal_amount = total_referal_amount + wei_value

    return total_referal_amount


@login_required(login_url='/login')
def UserProfile(request):
    try:
        context = {}
        own_points = 0
        current_user = User.objects.get(username=request.user)
        signup_user = SignUp.objects.get(user=current_user)
        context['myRefral'] = SignUp.objects.filter(sponsered_id=signup_user.referal_code)
        context['email'] = signup_user.user.username
        context['refral'] = signup_user.referal_code
        context['verify'] = signup_user.account_verified
        context['btc_add'] = signup_user.btc_address
        context['eth_add'] = signup_user.eth_address

        context['points'] = get_total_tokens_per_user(request.user)

        context['bonus'] = get_total_bonus_per_user(request.user)

        context['bonus'] += get_total_ether_bonus_per_user(request.user)

        context['points'] += get_total_ether_tokens_per_user(request.user)

        if request.method == 'POST':
            btc_add1 = request.POST.get("btcAddress")
            eth_add1 = request.POST.get("ethAddress")

            current_user = User.objects.get(username=request.user)
            signup_user = SignUp.objects.get(user=current_user)

            if btc_add1:
                signup_user.btc_address = btc_add1
                signup_user.save()
                context['messege'] = "Address Updated Successfully..!"

            if eth_add1 and len(eth_add1) == 42:
                signup_user.eth_address = eth_add1
                signup_user.save()
                context['messege'] = "Address Updated Successfully..!"
                return HttpResponseRedirect('/account')
    except Exception as e:
        print e

    return render(request, 'allAccount/account.html', context)


@login_required(login_url='/login')
def change_password(request):
    context = {}
    if request.method == 'POST':
        old_pass = request.POST.get("old_password")
        new_pass = request.POST.get("new_password")

        usr = User.objects.get(username=request.user)
        check_pass = usr.check_password(old_pass)
        if check_pass == True:
            usr.set_password(new_pass)
            usr.save()
            user = authenticate(username=request.user, password=new_pass)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/account')
                else:
                    return HttpResponseRedirect('/login')
        else:
            context['error'] = True
        # wrong pass error

    return render(request, 'change_password.html', context)


def forget_password(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get("email")
        check_user = User.objects.filter(username=email)
        if check_user:
            current_user = User.objects.get(username=email)
            signup_user = SignUp.objects.get(user=current_user)

            random_str = get_random_string(length=32)

            signup_user.pwd_verify_link = random_str
            signup_user.save()
            context['succ'] = True
            body_msg = "http://glico.io/pwd-verify/" + str(random_str)
            try:
                send_email = EmailMessage(
                    subject='Glico - Verify your account.',
                    body=body_msg,
                    from_email='care@glico.io',
                    to=[email],
                    reply_to=['care@glico.io'],
                    headers={'Content-Type': 'text/plain'},
                )
                send_email.send()
            except:
                pass
        else:
            context['succ'] = False
    return render(request, 'forget_password.html', context)


def password_link_verify(request, token):
    context = {}
    if request.method == 'GET':
        token = token
        find_user = SignUp.objects.filter(pwd_verify_link=token)
        if find_user:
            context['userTrue'] = True

    if request.method == 'POST':
        new_pass = request.POST.get('resetPass')
        try:
            user = SignUp.objects.get(pwd_verify_link=token)
            real_user = User.objects.get(username=user)
            real_user.set_password(new_pass)
            real_user.save()
            print "done"
        except:
            pass
    return render(request, 'pdw_verify.html', context)


def reset_password(request):
    if request.method == 'POST':
        token = str(request.POST.get('token')).split("/")
        pdw_confirm = token[-2]
        password = request.POST.get('resetPass')
        try:
            signup_user = SignUp.objects.get(pwd_verify_link=pdw_confirm)
            real_user = User.objects.get(username=signup_user)
            real_user.set_password(password)
            real_user.save()
        except Exception as e:
            print e
    return HttpResponseRedirect('/account')


@login_required(login_url='/login')
def verify_email(request, username):
    context = {}
    if len(username) > 2:
        is_user = SignUp.objects.filter(verify_link=username)
        if is_user > 0:
            user = SignUp.objects.get(verify_link=username)
            user.account_verified = True
            user.save()
            context['messege'] = "Account Verified Successfully !"
        else:
            pass
        # no user found
    return HttpResponseRedirect('/login')


@login_required(login_url='/login')
def wallet_history(request):
    context = {}
    usr = User.objects.get(username=request.user)
    signup_user = SignUp.objects.get(user=usr)
    all_transactions = Transactions.objects.filter(user=signup_user)
    # context['transactions'] = all_transactions
    return render(request, 'history.html', context)


@login_required(login_url='/login')
def generate_barcode(request):
    context = {}
    usr = User.objects.get(username=request.user)
    signup_user = SignUp.objects.get(user=usr)

    context['verify'] = signup_user.account_verified

    context['given'] = signup_user.eth_address
    eth = EtherumAddress.objects.all()
    # for b in bar:
    #     context['btc_addr'] = b.address

    for e in eth:
        context['eth_addr'] = e.address
    return render(request, 'generate_address.html', context)


def whitepaper(request):
    return render(request, 'whitepaper.html', {})


def token_sale(request):
    context = {}
    sale = TokenSale.objects.all()
    for s in sale:
        context['pre'] = s.pre_sale
        context['ico'] = s.ico
    return render(request, 'token_sale.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')


def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response


def payment_hander(request, invoice_id):
    address = request.GET.get('address')
    secret = request.GET.get('secret')
    confirmations = request.GET.get('confirmations')
    tx_hash = request.GET.get('transaction_hash')
    value = float(request.GET.get('value', 0)) / 100000000

    invoice_obj = Invoice.objects.filter(invoice_id=invoice_id).first()
    if invoice_obj:
        if address != invoice_obj.address:
            return HttpResponse('Incorrect Receiving Address', status=400)

        if secret != settings.PRIVATE_URL_KEY:
            return HttpResponse('invalid secret', 400)

        if confirmations >= 6:
            c_invoice_obj = InvoicePayment.objects.filter(transaction_hash=tx_hash).first()
            if not c_invoice_obj:
                today = datetime.datetime.now().date()
                c_invoice_obj = InvoicePayment.objects.create(
                    invoice=invoice_obj, transaction_hash=tx_hash, value=value)
                discount_obj = DiscountTable.objects.filter(
                    from_date__lte=today, 
                    to_date__gte=today,
                    currency_type=1
                    ).first()
                if discount_obj:
                    c_invoice_obj.btp_rate = discount_obj.btp_rate
                    c_invoice_obj.save()

                bonus_obj = BonusTable.objects.filter(from_date__lte=today, to_date__gte=today).first()
                if bonus_obj:
                    c_invoice_obj.bonus_percent = bonus_obj.percentage
                    c_invoice_obj.save()

            pending_invoice = PendingInvoicePayment.objects.filter(invoice=invoice_obj).first()
            if pending_invoice:
                pending_invoice.delete()
            return HttpResponse('*ok*')

        else:
            PendingInvoicePayment.objects.create(invoice=invoice_obj, transaction_hash=tx_hash, value=value)
            return HttpResponse('Waiting for confirmation')

    return HttpResponse("something went wrong", status=500)

# def token_count(request):
#     try:
#         signup_user_refrral = SignUp.objects.aggregate(Sum('referal_bonus'))
#         print "Bonus Tokens: ",signup_user_refrral['referal_bonus__sum']

#         all_transactions = Transactions.objects.filter(transaction_status='successful').aggregate(Sum('token'))
#         print "Owend Tokens: ", all_transactions['token__sum']

#         print "total Tokens: ", signup_user_refrral['referal_bonus__sum'] + all_transactions['token__sum']
#     except Exception as e:
#         print e

#     return render(request, 'token_count.html',{})

