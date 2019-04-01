from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from .models import Subscriber
from .forms import PhoneNumberForm, PhoneNumberVerifyForm
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from core.decorators import define_usage
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
import urllib.request as make_request
from django.conf import settings


#url /account
@login_required
def account_main(request):
    try: #User is a registered subscriber
        sub = request.user.subscriber
        if sub.active: #fully set up account
            form = PhoneNumberForm()
            """if sub.journal_set.count() == 0: #probably should be its own view, 4/4
                make_request.Request("https://smsjournal.xyz/journals/api/entry/",
                                     data={"names": "",
                                           "message": "Welcome to SMSJournal! You can make journal entries to this file by sending messages to the SMSJournal phone number, (970)-507-7992. To send an entry to a different journal, just add a tag like @ideas and we'll find or create the journal \"ideas\" in your Google Drive.",
                                           "phone": sub.phone,
                                           "api_key": settings.API_KEY},
                                     method="POST")"""
            return render(request, 'account_main.html', {'form': form, 'user_email': sub.user.email, 'username': sub.user.username, 'stripe_key': settings.STRIPE_PUBLISHABLE_KEY})
        elif sub.stripe_customer_id: #has paid, has not done first message
            return HttpResponseRedirect('/account/initialize_journal/')
        elif sub.phone_verified: #confirmed phone number but not paid
            return HttpResponseRedirect('/account/stripe_pay/')
        else: # Phone number not yet confirmed
            return HttpResponseRedirect('/account/phone_verify/')
    except: #user not a subscriber yet
        return HttpResponseRedirect('/account/phone_set/')


#url /account/phone_set/
@login_required
def phone_set(request):
    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        #Process and verify
        number = form.validate()
        if not number:
            if form.data["phone_number"] != form.data["phone_number_confirm"]:
                return render(request, 'phone_set.html', {'form': form, 'mismatchError': True})
            return render(request, 'phone_set.html', {'form': form, 'formatError': True})
        new_subscriber = Subscriber(user=request.user, phone=number)
        new_subscriber.save()
        new_subscriber.send_code()
        return HttpResponseRedirect('/account/phone_verify/')
    else:
        form = PhoneNumberForm()
        return render(request, 'phone_set.html', {'form': form})


#url /account/phone_verify/
@login_required
def phone_verify(request):
    if request.method == "POST":
        form = PhoneNumberVerifyForm(request.POST)
        #Process and verify
        #check_code mismatchError
        sub = request.user.subscriber
        if form.data["code"] == str(sub.verif_code):
            sub.phone_verified = True
            sub.save()
            return HttpResponseRedirect('/account/stripe_pay/')
        else:
            return render(request, 'phone_verify.html', {'form': form, 'mismatchError': True})
    else:
        form = PhoneNumberVerifyForm()
        return render(request, 'phone_verify.html', {'form': form})


#url /account/stripe_pay/
@login_required
def stripe_pay(request):
    return render(request, 'stripe_pay.html', {'username': request.user.username, 'stripe_key': settings.STRIPE_PUBLISHABLE_KEY})


#url /account/initialize_journal
@login_required
def initialize_journal(request):
    pass


# url
@define_usage(params={"stripeToken": "String", "username": "String"},
              returns={"Result": "String"})
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup_and_charge(request):
    try:
        sub = User.objects.get(username=request.data["username"]).subscriber
        sub.subscribe(request.data['stripeToken'])
        return Response({"Result": "Done"})
    except:
        return Response({"Result": "Something went wrong"})


@define_usage(params={"stripeToken": "String", "username": "String"},
              returns={"Result": "String"})
@api_view(["POST"])
@permission_classes((AllowAny,))
def stripe_card_change(request):
    try:
        print("in try")
        sub = User.objects.get(username=request.data["username"]).subscriber
        print(sub.user.username)
        print(request.data['stripeToken'])
        sub.change_card(request.data['stripeToken'])
        print(request.data['stripeToken'])
        return Response({"Result": "Done"})
    except:
        return Response({"Result": "Something went wrong."})


def unsubscribe(request):
    try:
        sub = User.objects.get(username=request.data["username"]).subscriber
        sub.delete_customer()
        sub.active = False
        sub.save()
    except:
        pass
    return render(request, 'index.html')


#this webhook can be set to be hit if payment fails. what do we do?
# add extra field to model if payment failed or not and wait till it works or fails next time?
@csrf_exempt
def stripe_web_hook(request):
    event_json = json.loads(request.body)
    phone = event_json["phone"]
    email = event_json["email"]
    charge_id = event_json["id"]
    email = EmailMessage(to=["info@grammiegram.com"],
                         from_email="smsjournalanalytics@grammiegram.com",
                         reply_to=["info@grammiegram.com"],
                         subject="Error receiving payment from SMS Journal!",
                         body="The charge {} has failed. Phone of the user: {}, email of the user: {}".format(charge_id, phone, email))
    email.send()
    return HttpResponse(status=200)
