from django.shortcuts import redirect, render
from rest_framework.views import APIView
from .forms import VoterRegistrationForm, VoterLoginForm

# Create your views here.
class RegisterVoterView(APIView):
    def get(self, request):
        form = VoterRegistrationForm()
        return render(request, 'voters/register.html', {'form': form})

    def post(self, request):
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('voters:registration_success')
        return render(request, 'voters/register.html', {'form': form})

class LoginVoterView(APIView):
    def get(self, request):
        form = VoterLoginForm()
        return render(request, 'voters/login.html', {'form': form})

    def post(self, request):
        form = VoterLoginForm(request.POST)
        token = request.data.get('token')
        if form.is_valid():
            # Authenticate user
            return redirect('voters:login_success')
        return render(request, 'voters/login.html', {'form': form})