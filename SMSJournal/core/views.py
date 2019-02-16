from django.shortcuts import render
from .models import Metrics, daily_metrics

# Basic Renders


def index(request):
    met = Metrics.objects.get(current=True)
    met.log_main_page_visit()
    return render(request, 'index.html')


def terms(request):
    return render(request, 'terms.html')


def privacy(request):
    return render(request, 'privacy.html')


def license(request):
    return render(request, 'license.html')


def metrics_job(request):
    if request.data["record"] == "yes": #make sure I don't trigger accidentally with page visit
        daily_metrics()
        return "Done"
    return "Nothing Happened"
