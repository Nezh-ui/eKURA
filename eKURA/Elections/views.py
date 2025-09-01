from email.mime import message
from pyexpat.errors import messages
from urllib import response
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect, render
from rest_framework.response import Response
from .models import Candidate, Vote
from .serializers import CandidateSerializer, User, VoterRegistrationSerializer
from .serializers import VoterLoginSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = VoterRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            voter = serializer.save()
            return Response({'message': 'Registration successful', 'voter': VoterRegistrationSerializer(voter).data})
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginVoterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VoterLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # ✅ sets session
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            print("DEBUG ERRORS:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_view(request, candidate_id):
    voter = request.user

    try:
        candidate = Candidate.objects.get(id=candidate_id)
    except Candidate.DoesNotExist:
        return Response({"message": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

    if Vote.objects.filter(voter=voter).exists():
        return Response({"message": "You have already voted"}, status=status.HTTP_400_BAD_REQUEST)

    Vote.objects.create(voter=voter, candidate=candidate)
    voter.voted = True
    voter.save()

    return Response({"message": "Vote recorded successfully"}, status=status.HTTP_201_CREATED)

class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [AllowAny]


class CandidateDetailView(generics.RetrieveAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [AllowAny]
