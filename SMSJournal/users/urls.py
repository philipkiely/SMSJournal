from django.urls import path
from . import views


urlpatterns = [
    path('', views.account_main, name='account_main'),
    path('phone_set/', views.phone_set, name='phone_set'),
    path('phone_verify/', views.phone_verify, name='phone_verify'),
    path('check_code/', views.check_code, name='check_code'),
    path('stripe_pay/', views.stripe_pay, name='stripe_pay'),
    path('signup_and_charge/', views.signup_and_charge, name='signup_and_charge'),
    path('stripe_webhook/', views.stripe_web_hook, name='stripe_webhook'),
    path('stripe_change_card/', views.stripe_card_change, name="card_change"),
    path('unsubscribe/', views.unsubscribe, name="unsubscribe"),
]
