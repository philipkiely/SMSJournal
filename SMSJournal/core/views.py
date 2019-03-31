from django.shortcuts import render
from .models import Metrics, daily_metrics, Subscriber
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from core.decorators import define_usage
from django.conf import settings
import stripe
from django.http import HttpResponse
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
# this goes to user
from django.core.mail import EmailMessage
# Basic Renders


# url /
def index(request):
    try: #make sure the page always loads
        met = Metrics.objects.get(current=True)
        met.log_main_page_visit()
    except:
        pass
    return render(request, 'index.html')


# url /terms
def terms(request):
    return render(request, 'terms.html')


#url /privacy
def privacy(request):
    return render(request, 'privacy.html')


#url /license
def license(request):
    return render(request, 'license.html')


# API Call

# url api_daily_metrics
@define_usage(params={"api_key": "String"},
              returns={"Result": "String"})
@api_view(["POST"])
@permission_classes((AllowAny,))
def api_daily_metrics(request):
    if request.data["api_key"] != settings.API_KEY: #will be env variable in settings
        return Response({"Result": "API Key Incorrect"})
    daily_metrics()
    return Response({"Result": "Done"})


# url / first_charge
@define_usage(params={"stripeToken": "String", "username":"String"},
              returns={"Result": "String"})
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup_and_charge(request):
    try: 
        token = request.data['stripeToken']
        username=request.data["username"]
        usr = User.objects.get(username=username)
        sub = Subscriber.objects.get(user=usr)
        sub.subscribe(token)
        return Response({"Result": "Done"})
    except:
        return Response({"Result": "Something went wrong"})



@define_usage(params={"stripeToken": "String","username":"String"},
              returns={"Result": "String"})
@api_view(["POST"])
@permission_classes((AllowAny,))
def stripe_card_change(request):
    try: 
        token = request.data['stripeToken']
        username=request.data["username"]
        usr = User.objects.get(username=username)
        sub = Subscriber.objects.get(user=usr)
        sub.change_card(token)
        return Response({"Result": "Done"})
    except:
        return Response({"Result": "Something went wrong."})



def unsubscribe(request): 
    try:
        username=request.POST["username"]
        usr = User.objects.get(username=username)
        sub = Subscriber.objects.get(user=usr)
        sub.delete_customer()
        sub.active = True
        sub.save()
    except:
        print("Weird")
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
                         body="The charge {} has failed. Phone of the user: {}, email of the user: {}".format(charge_id,phone,email))
    email.send()

    return HttpResponse(status=200)



def stripe_playground_remove_it(request):
    return render(request, 'stripe_playground.html',{"stripe_key":settings.STRIPE_PUBLISHABLE_KEY, "username": "user1"})

def stripe_account_remove_it(request):
    return render(request, 'stripe_account_playground.html',{"stripe_key":settings.STRIPE_PUBLISHABLE_KEY, "username": "user1", "user_email" : "email@buubu.com"})