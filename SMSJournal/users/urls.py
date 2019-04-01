from django.urls import path
from . import views


urlpatterns = [
    path('', views.account_main, name='account_main'),
    path('phone_set/', views.phone_set, name='phone_set'),
    path('phone_verify/', views.phone_verify, name='phone_verify'),
    path('stripe_pay/', views.stripe_pay, name='stripe_pay'),
    path('check_code/', views.check_code, name='check_code'),
]
