from django.urls import path
from . import views


urlpatterns = [
    path('', views.account_main, name='account_main'),
    path('check_code/', views.check_code, name='check_code'),
]
