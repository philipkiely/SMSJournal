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
            if sub.journal_set.count() == 0: #probably should be its own view, 4/4
                make_request.Request("https://smsjournal.xyz/journals/api/entry/",
                                     data={"names": "",
                                           "message": "Welcome to SMSJournal! You can make journal entries to this file by sending messages to the SMSJournal phone number, (970)-507-7992. To send an entry to a different journal, just add a tag like @ideas and we'll find or create the journal \"ideas\" in your Google Drive.",
                                           "phone": sub.phone,
                                           "api_key": settings.API_KEY},
                                     method="POST")
            return render(request, 'account_main.html', {'form': form})
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
        new_subscriber = Subscriber(user=request.user, phone=number, verif_code=123456, active=True)
        new_subscriber.save()
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
        if form.data["code"] == str(123456):
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


'''
User inputs the phone number:
-> save number into user's model
-> call send_code, it adds a random verif. code
to the model too
-> once user inputs the code, call check_code
-> if the code is correct, verif.code is set to null
we can use this to see if phone is verified:
code ==null => verified, otherwise no

'''


def check_code(request):
    usr_id = request.POST.get('usr_id')
    subscriber_usr = User.objects.get(username=usr_id)
    subscriber = Subscriber.objects.get(user=subscriber_usr)
    submitted_code = request.POST.get('code')
    try:
        if subscriber.code == submitted_code:
            subscriber.phone_number = request.POST.get('phone')
            subscriber.verif_code = None
            return redirect('/success/')
    except:
        print("No code field for user {}".format(usr_id))
    return render(request, 'some/url', {'error': 'Wrong code from the number'})


# url / first_charge
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
        sub = User.objects.get(username=request.data["username"]).subscriber
        sub.change_card(request.data['stripeToken'])
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
