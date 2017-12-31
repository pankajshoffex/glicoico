from django.conf.urls import url
from .views import ComingSoon, HomePage, login_in_account, signup, UserProfile, logout_view, generate_barcode, \
    token_sale, change_password, forget_password, password_link_verify, reset_password, wallet_history, calculator, \
    whitepaper, GetUserAddress, payment_hander

urlpatterns = [
    # url(r'^$', HomePage, name="HomePage"),
    url(r'^login', login_in_account, name="login"),
    url(r'^signup$', signup, name="signup"),
    url(r'^signup/(?P<page>\w+)$', signup, name="signup"),
    url(r'^account', UserProfile, name="userprofile"),
    url(r'^logout', logout_view, name="logout"),
    url(r'^contribute', generate_barcode, name="contribute"),
    url(r'^token-sale', token_sale, name="token_sale"),
    url(r'^change-password', change_password, name="change_password"),
    url(r'^forget-password', forget_password, name="forget_password"),
    url(r'^pwd-verify/(?P<token>\w{0,50})/$', password_link_verify, name="pwd_verify"),
    url(r'^reset-password', reset_password, name="reset_password"),
    url(r'^history', wallet_history, name="history"),
    url(r'^cal', calculator, name="cal"),
    url(r'^whitepaper', whitepaper, name="whitepaper"),
    url(r'^get-address', GetUserAddress, name="getuseraddress"),
    url(r'^payment/(?P<invoice_id>\d+)/$', payment_hander, name="payment"),
]

