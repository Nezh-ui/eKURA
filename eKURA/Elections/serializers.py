from email import message
import token
from urllib import response
from rest_framework import serializers
from .models import Vote, Candidate, Voter
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=100, required=True)
    national_id = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=Voter.objects.all())])

    def create(self, validated_data):
        voter = get_user_model().objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            national_id=validated_data['national_id']
        )
        Token.objects.create(user=voter)
        return Response({'token': token.key, 'message': "User created successfully"})

class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.StringRelatedField()
    candidate = serializers.StringRelatedField()
    election = serializers.StringRelatedField()

    class Meta:
        model = Vote
        fields = ['voter', 'candidate', 'election']

    def validate(self, attrs):
        voter = self.context['request'].user
        candidate = attrs['candidate']
        election = attrs['election']

        if Vote.objects.filter(voter=voter, candidate=candidate, election=election).exists():
            raise serializers.ValidationError("You have already voted for this candidate in this election.")
        if not voter.is_authenticated:
            raise serializers.ValidationError("You must be logged in to vote.")
        return attrs

    def create(self, validated_data):
        validated_data['voter'] = self.context['request'].user
        return super().create(validated_data)

class CandidateSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(source='vote_count', read_only=True)

    class Meta:
        model = Candidate
        fields = ['name', 'party', 'election', 'vote_count']

    def get_vote_count(self, obj):
        return obj.votes.count()

class VoterRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    national_id = serializers.CharField(max_length=100)

    class Meta:
        model = Voter
        fields = ['email', 'password', 'national_id']

    def create(self, validated_data):
        voter = get_user_model().objects.create_user(
            username=validated_data['national_id'],
            email=validated_data['email'],
            password=validated_data['password'],
            national_id=validated_data['national_id']
        )
        Token.objects.create(user=voter)
        return Voter.objects.create(user=voter, national_id=validated_data['national_id'])

class VoterLoginSerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = Voter
        fields = ['national_id', 'password']

    def validate(self, data):
        national_id = data.get('national_id')
        password = data.get('password')
        if national_id and password:
            user = authenticate(request=self.context.get('request'),
                                national_id=national_id, password=password)
            if user is not None:
                return user
            raise serializers.ValidationError("Invalid credentials.")
        raise serializers.ValidationError("All fields are required.")
        return data

