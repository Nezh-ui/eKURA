from django.urls import path
from django.contrib import admin
from .views import RegisterVoterView, LoginVoterView

urlpatterns = [
    path('register/', RegisterVoterView.as_view(), name='register'),
    path('login/', LoginVoterView.as_view(), name='login'),
    
]