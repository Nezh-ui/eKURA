from django import forms
from .models import Voter


class VoterRegistrationForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['name', 'email', 'age', 'national_id', 'location']

class VoterLoginForm(forms.Form):
    email = forms.EmailField()
    national_id = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    