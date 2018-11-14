from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebook = models.URLField(max_length=500, unique=True)
    status = models.TextField(max_length=254, blank=True)

