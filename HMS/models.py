from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class AccountType(models.TextChoices):
    CUSTOMER = 'Customer'
    HOTEL_MANAGER = 'Hotel Manager'
    ADMIN = 'Admin'

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=64)
    account_type = models.CharField(max_length=20,choices=AccountType.choices,default=AccountType.CUSTOMER,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
    