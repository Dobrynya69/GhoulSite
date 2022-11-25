from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    zxc_scores = models.SmallIntegerField(default=1000)
    zxc_level = models.PositiveSmallIntegerField(default=1)
    active_email = models.BooleanField(default=False)