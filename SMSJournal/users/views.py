from django.shortcuts import render
from django.http import HttpResponseRedirect
import os
from django.conf import settings
from django.shortcuts import redirect
from .models import Subscriber
from .forms import PhoneNumberForm, PhoneNumberVerifyForm
from django.contrib.auth.decorators import login_required


#url /account
@login_required
def account_main(request):
    try: #User is a registered subscriber
        sub = request.user.subscriber
        if sub.active: #fully set up account
            return render(request, 'account_main.html')
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
    return render(request, 'stripe_pay.html')

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
