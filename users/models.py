from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birthdate = models.DateField()
    is_employee = models.BooleanField(default=False)
