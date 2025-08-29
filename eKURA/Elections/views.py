from pyexpat.errors import messages
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect, render
from rest_framework.response import Response
from .models import Candidate, Vote
from .forms import VoterRegistrationForm, VoterLoginForm
from .serializers import CandidateSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return Response({'message': 'Registration successful'})
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginVoterView(APIView):
    def post(self, request):
        form = VoterLoginForm(request.POST)
        if form.is_valid():
            national_id = form.cleaned_data['national_id']
            password = form.cleaned_data['password']
            user = authenticate(request, national_id=national_id, password=password)
            if user is not None:
                login(request, user)
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

class CandidateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

class CandidateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, candidate_id):
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data)
        except Candidate.DoesNotExist:
            return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)