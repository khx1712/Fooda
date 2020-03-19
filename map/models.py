from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
    CATEGORIES = (
        ('K', 'Korean'),
        ('J', 'Japanese'),
        ('C', 'Chinese'),
        ('W', 'Western'),
        ('A', 'Asian'),
        ('E', 'Southeast_Asia'),
        ('S', 'South_America'),
        ('M', 'Mideast'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=50)
    location = models.TextField(max_length=100)
    category = models.CharField(max_length=1, choices=CATEGORIES, blank=True)
    business_hour = models.TextField(max_length=100, blank=True)
    menu = models.TextField(max_length=100, blank=True)

    #def __str__(self):
    #    return self.user. + " " + self.name

    #class Meta:
    #    ordering = ['-user']