from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
import requests
import json
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.core.cache import caches

# from account.models import Profile
from .models import TransactionAmount
from django.contrib.auth.decorators import login_required
from .models import Payment

cache = caches.create_connection("default")

MERCHANT = 'e6aa22b0-132a-4de3-976e-918097ce01e6'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09130666144'  # Optional
# if settings.ENV["REAL_SERVER"]:
#     CallbackURL = 'http://c2oo.ir/pay/verify/'
# else:
CallbackURL = 'http://127.0.0.1:8000/pay/verify/'


# @login_required(login_url="/account/login")
def send_request(request):
    amount = int(request.GET.get("w", 0)) * 10
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        obj = Payment(amount=amount / 10, transaction_id=authority, user_id=request.user.id)
        obj.save()
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required(login_url="/account/login")
def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    pending_payment = Payment.objects.all().filter(transaction_id=t_authority, user_id=request.user.id).first()
    if t_status == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": pending_payment.amount * 10,
            "authority": t_authority,
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                # return HttpResponse('Transaction success.\nRefID: ' + str(
                #     req.json()['data']['ref_id']
                # ))
                pending_payment.status = "success"
                pending_payment.save()
                profile = Profile.objects.filter(user_id=request.user.id).first()
                profile.balance += pending_payment.amount
                profile.save()
                messages.success(request, "کیف پول  شما با موفقیت شارژ شده است.")
                user_flow_in_redis = cache.get(f"user_id_{request.user.id}", None)
                if user_flow_in_redis:
                    return HttpResponseRedirect(reverse("handle_flow", kwargs={"hash": user_flow_in_redis}))
                else:
                    return HttpResponseRedirect("/")
            elif t_status == 101:
                pending_payment.status = "failed"
                pending_payment.save()
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                pending_payment.status = "failed"
                pending_payment.save()
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            pending_payment.status = "failed"
            pending_payment.save()
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        # payment cancelled
        pending_payment.status = "failed"
        pending_payment.save()
        return HttpResponse('Transaction failed or canceled by user')


@login_required(login_url="/account/login")
def add_balance(request):
    profile = Profile.objects.filter(user_id=request.user.id).first()
    if profile.skill_count == 1:
        transaction_amount = TransactionAmount.objects.all().values_list("amount", flat=True)
    else:
        transaction_amount = TransactionAmount.objects.all().first()
        if transaction_amount:
            transaction_amount = [transaction_amount.amount * profile.skill_count]
    balance = profile.balance
    context = {
        "transaction_amount": transaction_amount,
        "balance": balance,
    }
    if request.POST:
        amount = request.POST.get("amount")
        if amount.__contains__(","):
            cleaned_amount = amount.replace(",", "").replace(")", "").replace("(", "")
            cleaned_amount = int(cleaned_amount.split("تومان")[1])
        else:
            try:
                cleaned_amount = int(amount.replace("تومان", "").strip())
            except:
                return HttpResponseRedirect(reverse("add_balance"))
        try:
            return HttpResponseRedirect(
                reverse("request") + "?" + "w=" + str(cleaned_amount))
        except:
            messages.success(request, "مقادیر ورودی صحیح نمی باشد.")
            return HttpResponseRedirect(reverse("add_balance"))
    return render(request, "zarinpal/add_balance.html", context)
