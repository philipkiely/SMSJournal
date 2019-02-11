from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.api_root, name='api_root'),
    path('api/create_journal/', views.api_create_journal, name='api_create_journal'),
    path('api/get_journal/', views.api_get_journal, name='api_get_journal'),
]
