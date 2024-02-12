from django.db import models
from django.contrib.auth.models import AbstractUser

class User(models.Model):
    userid = models.AutoField(primary_key=True, auto_created=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.username)
