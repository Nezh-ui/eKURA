from django import forms
from .models import Voter


class VoterRegistrationForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['name', 'age', 'national_id', 'password']

class VoterLoginForm(forms.Form):
    username = forms.CharField(label='national_id', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    