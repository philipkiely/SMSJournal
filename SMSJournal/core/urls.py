from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('license/', views.license, name='license'),
    path('api_daily_metrics/', views.api_daily_metrics, name='api_daily_metrics'),
    path('first_charge/', views.first_charge, name='first_charge'),
]
