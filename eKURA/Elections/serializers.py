from email import message
import token
from urllib import response
from rest_framework import serializers
from .models import Vote, Candidate, Voter
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login

User = get_user_model()

class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['voter', 'candidate', 'timestamp']

    def validate(self, attrs):
        voter = self.context['request'].user
        candidate = attrs['candidate']

        if Vote.objects.filter(voter=voter, candidate=candidate).exists():
            raise serializers.ValidationError("You have already voted for this candidate.")
        if not voter.is_authenticated:
            raise serializers.ValidationError("You must be logged in to vote.")
        return attrs

    def create(self, validated_data):
        validated_data['voter'] = self.context['request'].user
        return super().create(validated_data)

class CandidateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'party']


class VoterRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    national_id = serializers.CharField(max_length=100)

    class Meta:
        model = Voter
        fields = ['email', 'password', 'national_id', 'age']

    def validate_email(self, value):
        if Voter.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    
    def validate_national_id(self, value):
        if Voter.objects.filter(national_id=value).exists():
            raise serializers.ValidationError("National ID is already in use.")
        return value

    def create(self, validated_data):
        voter = get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            national_id=validated_data['national_id'],
            age=validated_data['age']
        )
        voter.set_password(validated_data['password'])
        voter.save()
        return voter

class VoterLoginSerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

    def validate(self, data):
        national_id = data.get("national_id")
        password = data.get("password")
        User = get_user_model()

        try:
            user = User.objects.get(national_id=national_id)
            if not user.check_password(password):
                raise serializers.ValidationError("Invalid password.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        data["user"] = user
        return data
