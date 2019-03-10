from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('check_code/', views.check_code, name='check_code'),
    path('', include('social_django.urls', namespace='social_auth')),
    path('logout/', auth_views.LogoutView, {'next_page': settings.LOGOUT_REDIRECT_URL},
         name='logout'),
]
