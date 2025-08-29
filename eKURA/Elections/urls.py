from django.urls import path
from .views import  CandidateAPIView, CandidateListView, LoginVoterView, RegistrationView, vote
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginVoterView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('vote/<int:candidate_id>/', vote, name='vote'),
    path('candidates/', CandidateListView.as_view(), name='candidate_list'),
    path('candidates/<int:candidate_id>/', CandidateAPIView.as_view(), name='candidate_detail'),
]