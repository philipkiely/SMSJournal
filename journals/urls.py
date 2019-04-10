from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.api_root, name='api_root'),
    path('api/entry/', views.api_journal_entry, name='api_journal_entry'),
]
