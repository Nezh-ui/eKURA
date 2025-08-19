from django.db import models

# Create your models here.
class Voter(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    ID = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
