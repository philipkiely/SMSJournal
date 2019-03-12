from django.shortcuts import render
from .models import Metrics, daily_metrics, Subscriber
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from core.decorators import define_usage
from django.conf import settings
import stripe
from django.http import HttpResponse
# Basic Renders


# url /
def index(request):
    try: #make sure the page always loads
        met = Metrics.objects.get(current=True)
        met.log_main_page_visit()
    except:
        pass
    return render(request, 'index.html',{"stripe_key":settings.STRIPE_PUBLISHABLE_KEY})


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
def first_charge(request): 
    if request.method == 'POST':
        usr = User(username="test1", password="test1")
        token = request.POST['stripeToken']
        #user = Subscriber.objects.get(phone=request.POST["phone"])
        sub = Subscriber(user=usr,phone=request.POST["phone"], )
        user.subscribe(token)

    print("Person was charged first charge")
    return render(request, 'success.html')