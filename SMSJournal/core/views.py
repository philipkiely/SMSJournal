from django.shortcuts import render

# Basic Renders


def index(request):
    return render(request, 'index.html')


def terms(request):
    return render(request, 'terms.html')


def privacy(request):
    return render(request, 'privacy.html')


def license(request):
    return render(request, 'license.html')
