from django.urls import path
from .views import  CandidateAPIView, LoginVoterView, RegistrationView, CandidateListCreateView, vote_view
from django.contrib.auth import views as auth_views

app_name = 'Elections'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginVoterView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('vote/<int:candidate_id>/', vote_view, name='vote'),
    path('candidates/', CandidateListCreateView.as_view(), name='candidate-list_create'),
    path('candidates/<int:candidate_id>/', CandidateAPIView.as_view(), name='candidate_detail'),
]