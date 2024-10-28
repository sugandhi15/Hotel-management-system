from .models import User,Room,Booking
from rest_framework import serializers

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        models = Booking
        fields = '__all__'

