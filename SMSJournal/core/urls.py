from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('license/', views.license, name='license'),
    path('api_daily_metrics/', views.api_daily_metrics, name='api_daily_metrics'),
    path('signup_and_charge/', views.signup_and_charge, name='signup_and_charge'),
    path('stripe_webhook/', views.stripe_web_hook, name='stripe_webhook'),
    path('stripe/', views.stripe_playground_remove_it, name="stripe"),
    path('stripe_account/', views.stripe_account_remove_it, name="stripe_account"),
    path('stripe_change_card/', views.stripe_card_change, name="card_change"),
    path('unsubscribe/', views.unsubscribe, name="unsubscribe"),
]
