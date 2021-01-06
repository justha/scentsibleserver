from django.db import models
from django.contrib.auth.models import User

class ScentsibleUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

@property
def username(self):
    return self.user.username

@property
def currentuser(self):
    return self.__currentuser

@currentuser.setter
def currentuser(self,value):
    self.__currentuser = value