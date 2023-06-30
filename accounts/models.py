from django.db import models
from django.contrib.auth.models import AbstractUser
from Nutstore.models import City


class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    city = models.ForeignKey(City, null=True, blank=False ,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11)  #09121234567
    address = models.CharField(max_length=500)
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.username
