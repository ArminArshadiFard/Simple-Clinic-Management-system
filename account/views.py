from django.shortcuts import render, HttpResponseRedirect, reverse
import json
import random
import requests
import unidecode
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib import messages


def send_sms(mobile, code):
    url = "https://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber"
    payload = json.dumps({
        "username": "29378953656",
        "password": "2b7gd9c",
        "text": code,
        "to": mobile,
        "bodyId": "165914"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))

    if request.POST:
        hide_mobile = request.POST.get("hide_mobile", None)
        if hide_mobile:
            code = request.POST.get("code")
            user = authenticate(request, username=hide_mobile, password=code)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("dashboard"))
            else:
                messages.success(request, "کد وارد شده صحیح نیست.")
                return HttpResponseRedirect(reverse("login"))
        else:
            mobile = request.POST.get("mobile")
            # generate code
            make_code = random.randint(11111, 99999)
            # optional: you had make_code = 55555 hardcoded; maybe for testing
            # make_code = 55555

            # Print to terminal
            print(f"Generated login code for mobile {mobile} is: {make_code}")
            # ## or using logging (better)
            # import logging
            # logger = logging.getLogger(__name__)
            # logger.info(f"Generated login code for mobile {mobile}: {make_code}")

            # validate mobile
            if len(mobile) != 11 or not mobile.isdigit():
                messages.success(request, "شماره وارد شده معتبر نیست.")
                return render(request, "account/login.html")

            existence = User.objects.filter(username=mobile).last()
            if existence:
                existence.set_password(str(make_code))
                existence.save()
            else:
                obj = User.objects.create_user(username=mobile, password=str(make_code), first_name=mobile)
                obj.save()

            return render(request, "account/login.html", {'hide_mobile': mobile})

    return render(request, "account/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "شما از حساب کاربری خود خارج شدید.")
    return HttpResponseRedirect(reverse('login'))
