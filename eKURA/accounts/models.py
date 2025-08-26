from django.db import models
from django.contrib.auth.models import AbstractUser
from Elections.models import Election

# Create your models here.
class Voter(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=20, unique=True)
    age = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    voted = models.BooleanField(default=False)

    USERNAME_FIELD = 'national_id' 
    REQUIRED_FIELDS = [ 'email', 'name', 'age', 'location']

    def __str__(self):
        return self.username

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name