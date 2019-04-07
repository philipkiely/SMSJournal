from django.shortcuts import render
from .models import Metrics, daily_metrics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from core.decorators import define_usage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
import json
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


@csrf_exempt
def stripe_web_hook(request):
    event_json = json.loads(request.body)
    try:
        data = event_json["object"]
        charge_id = data["id"]
        email = data["billing_details"]["name"]
        email = EmailMessage(to=["info@grammiegram.com"],
                            from_email="smsjournalanalytics@grammiegram.com",
                            reply_to=["info@grammiegram.com"],
                            subject="Error receiving payment from SMS Journal!",
                            body="The charge {} has failed. Email of the user: {}".format(charge_id, email))
        email.send()
    except:
        email = EmailMessage(to=["info@grammiegram.com"],
                            from_email="smsjournalanalytics@grammiegram.com",
                            reply_to=["info@grammiegram.com"],
                            subject="Error receiving payment from SMS Journal!",
                            body="The undetermined error occured. The response from stripe:\n {}".format(json.dumps(event_json)))
        email.send()
    return HttpResponse(status=200)