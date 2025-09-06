from django.urls import path
from .views import LoginView, RegistrationView, vote_view, CandidateViewset
from django.contrib.auth import views as auth_views

app_name = 'Elections'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('vote/<int:candidate_id>/', vote_view, name='vote'),
    path('candidates/', CandidateViewset.as_view({'get': 'list', 'post': 'create'}), name='candidates'),
]