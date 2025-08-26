from django.urls import path
from .views import LoginVoterView, vote
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginVoterView.as_view(), name='login'),
    path('vote/<int:candidate_id>/', vote, name='vote'),
]