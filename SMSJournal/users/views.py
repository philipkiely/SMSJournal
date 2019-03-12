from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
from django.shortcuts import redirect
from .models import Subscriber
from .forms import PhoneNumberForm
from django.contrib.auth.decorators import login_required


@login_required
def account_main(request):
    try: #User is a registered subscriber
        sub = request.user.subscriber
        if sub.active:
            return render(request, 'account_main.html')
        else: #registration is not complete
            if request.method == "POST":
                form = PhoneNumberForm(request.POST, user=request.user)
                #Process and verify
                return render(request, 'account_main.html')
            else:
                form = PhoneNumberForm(user=request.user)
                return render(request, 'account_create.html')
    except:
        if request.method == "POST":
            form = PhoneNumberForm(request.POST, user=request.user)
            #Process and verify
            return render(request, 'account_main.html')
        else:
            form = PhoneNumberForm(user=request.user)
            return render(request, 'account_create.html')



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
