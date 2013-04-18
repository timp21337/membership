from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Member(models.Model):
    user = models.OneToOneField(User)

    dob = models.DateField()
