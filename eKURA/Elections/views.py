from rest_framework.authtoken.models import Token
from django.shortcuts import redirect, render
from rest_framework.response import Response
from .models import Vote
from .forms import VoterRegistrationForm, VoterLoginForm
from .serializers import VoterLoginSerializer,VoteSerializer
from rest_framework.generics import GenericAPIView
from django.contrib.auth.decorators import login_required
from rest_framework import status

class RegisterVoterView(GenericAPIView):
    def get(self, request):
        form = VoterRegistrationForm()
        return render(request, 'voters/register.html', {'form': form})

    def post(self, request):
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('voters:registration_success')
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
    
class VoteView(GenericAPIView):
    queryset = Vote.objects.all()
    serializer = VoteSerializer

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)