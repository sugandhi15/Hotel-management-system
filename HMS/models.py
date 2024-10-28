from django.db import models
from django.contrib.auth.models import AbstractBaseUser




# User schema
# allows us to get organised code and reusable components and alos provide only these choices to choose in.
class AccountType(models.TextChoices):
    CUSTOMER = 'Customer'
    HOTEL_MANAGER = 'Hotel Manager'
    ADMIN = 'Admin'

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=64)
    account_type = models.CharField(max_length=20,choices=AccountType.choices,default=AccountType.CUSTOMER,)

    USERNAME_FIELD = 'email'

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
    customer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.RESERVED)

    def __str__(self):
        return f"Room {self.room.room_no} - {self.status}"