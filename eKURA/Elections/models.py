from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

# Elections/models.py
from django.contrib.auth.models import BaseUserManager

class VoterManager(BaseUserManager):
    def create_user(self, national_id, email, age, password=None, **extra_fields):
        if not national_id:
            raise ValueError("The National ID must be set")
        if not email:
            raise ValueError("The Email must be set")

        email = self.normalize_email(email)
        user = self.model(national_id=national_id, email=email, age=age, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, national_id, email, age, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(national_id, email, age, password, **extra_fields)

class Voter(AbstractUser):
    username = None  # Remove the username field
    national_id = models.CharField(max_length=100, unique=True )
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    voted = models.BooleanField(default=False)

    objects = VoterManager()

    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = ['email', 'age']

    def __str__(self):
        return self.national_id



class Candidate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    manifesto = models.TextField(max_length=1000)
    vote_count = models.IntegerField(default=0)

    def get_vote_count(self):
        return self.vote_count

    def __str__(self):
        return self.name

class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        unique_together = ('voter', 'candidate') # Ensure a voter can vote for a candidate only once

    def vote(self, voter):
        if voter.voted:
            raise ValueError("This voter has already voted.")
        voter.voted = True
        voter.save()
        self.save()
