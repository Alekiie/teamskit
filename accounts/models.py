from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    ROLE_OPTIONS = [("Admin", "Admin"), ("Manager", "Manager"), ("Member", "Member")]
    role = models.CharField(max_length=55, choices=ROLE_OPTIONS, default="Member")

    def __str__(self):
        return f"{self.username} - ({self.role})"
