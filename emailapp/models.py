from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserInfo(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=50, null=False)
    host = models.CharField(max_length=50, null=False)
    port = models.CharField(max_length=5, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
