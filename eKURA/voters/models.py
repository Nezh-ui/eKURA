from django.db import models

# Create your models here.
class Voter(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    ID = models.ManyToManyField('self', related_name='voters', blank=True)
    age = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    voted = models.BooleanField(default=False)

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)

class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'candidate') # Ensure a voter can vote for a candidate only once
    
    def save(self, *args, **kwargs):
        if self.voter.voted:
            raise ValueError("This voter has already voted.")
        self.voter.voted = True
        self.voter.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.voter.name} voted for {self.candidate} on {self.timestamp}"