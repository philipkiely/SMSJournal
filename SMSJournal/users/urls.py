from django.urls import path
from . import views


urlpatterns = [
    path('check_code/', views.check_code, name='check_code'),
]
