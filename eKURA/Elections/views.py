from rest_framework.authtoken.models import Token
from django.shortcuts import redirect, render
from rest_framework.response import Response
from .models import Candidate, Vote
from .forms import VoterRegistrationForm, VoterLoginForm
from .serializers import VoterLoginSerializer,VoteSerializer
from rest_framework.generics import GenericAPIView
from django.contrib.auth.decorators import login_required
from rest_framework import status

def register(request):
    if request.method == 'POST':
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('voters:registration_success')
    else:
        form = VoterRegistrationForm()
    return render(request, 'voters/register.html', {'form': form})

class LoginVoterView(GenericAPIView):
    def get(self, request):
        form = VoterLoginForm()
        return render(request, 'voters/login.html', {'form': form})

    def post(self, request):
        form = VoterLoginForm(request.POST)
        serializer = VoterLoginSerializer(data=request.data)
        if serializer.is_valid(): 
            national_id = serializer.validated_data.get('ID')
            Token.objects.get_or_create(user__ID=national_id)
            return redirect('voters:login_success')
        return render(request, 'voters/login.html', {'form': form})
    
@login_required
def vote(request, candidate_id):
    voter = request.user
    candidate = Candidate.objects.get(id=candidate_id)

    if request.method == 'POST':
        vote = Vote(voter=voter, candidate=candidate)
        vote.save()
        return redirect('voters:vote_success')
    return render(request, 'voters/vote.html', {'candidate': candidate})