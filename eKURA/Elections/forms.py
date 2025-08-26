from django import forms
from .models import Voter


class VoterRegistrationForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['name', 'email', 'age', 'ID', 'location']

class VoterLoginForm(forms.Form):
    email = forms.EmailField()
    ID = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    