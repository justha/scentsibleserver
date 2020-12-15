from django.db import models

class Rating(models.Model):
    name = models.CharField(max_length=25)
    weight = models.IntegerField()