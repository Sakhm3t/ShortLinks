from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Links(models.Model):

    full_link = models.TextField()
    short_link = models.CharField(max_length=20, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)

