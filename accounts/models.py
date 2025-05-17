from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('shipper', 'Shipper'),
        ('driver', 'Driver'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
