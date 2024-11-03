from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)



# User schema
# allows us to get organised code and reusable components and alos provide only these choices to choose in.
class AccountType(models.TextChoices):
    CUSTOMER = 'Customer'
    HOTEL_MANAGER = 'Hotel Manager'
    ADMIN = 'Admin'

class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=64)
    account_type = models.CharField(max_length=20,choices=AccountType.choices,default=AccountType.CUSTOMER)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    




# hotel schema
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    hotel_id = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.name} {self.hotel_id}"





# room schema
class RoomType(models.TextChoices):
    SINGLE = 'Single'
    DOUBLE = 'Double'

class Availability(models.TextChoices):
        AVAILABLE = 'Available'
        BOOKED = 'Booked'

class Room(models.Model):
    hotel = models.ForeignKey('Hotel',on_delete=models.CASCADE,related_name="rooms")
    room_no = models.IntegerField()
    room_type = models.CharField(max_length=20,choices=RoomType.choices)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    availability = models.CharField(max_length=20,choices=Availability.choices,default=Availability.AVAILABLE)
    bookings = models.ManyToManyField('Booking', related_name='rooms', blank=True)

    def __str__(self):
        return f"Room {self.room_no} ({self.room_type})"






# Booking schema
class Status(models.TextChoices):
    RESERVED = 'Reserved'
    CHECKED_IN = 'Checked-In'
    CHECKED_OUT = 'Checked-Out'

class Booking(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey('Room', on_delete=models.CASCADE,related_name='rooms')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.RESERVED)

    def __str__(self):
        return f"Room {self.room.room_no} - {self.status}"