from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('license/', views.license, name='license'),
    path('daily_metrics/', views.daily_metrics, name='daily_metrics'),
]
