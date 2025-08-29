from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class Election(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    election = models.ForeignKey(Election, on_delete=models.CASCADE) 
    

    def __str__(self):
        return self.name

class Voter(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=20, unique=True)
    age = models.PositiveIntegerField()
    password = models.CharField(max_length=100)
    voted = models.BooleanField(default=False)

    USERNAME_FIELD = 'national_id' 
    REQUIRED_FIELDS = [ 'email', 'name', 'age' 'password']

    def __str__(self):
        return self.username

class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        unique_together = ('voter', 'candidate', 'election') # Ensure a voter can vote for a candidate only once in an election

    def vote(self, voter):
        if voter.voted:
            raise ValueError("This voter has already voted.")
        voter.voted = True
        voter.save()
        self.save()