# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .serializer import Userserializer,RoomSerializer,BookingSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Hotel
from django.core.mail import send_mail
from django.template.loader import render_to_string

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def home(request):
    serializer = Userserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



#  to reset password without token
@api_view(['POST'])
def ResetPassword(request):
    try:
        email = request.data.get('email')
        if not email:
            return Response({
                "error": "Email is required."
            })
        user = User.objects.get(email=email)
        password_reset_link = "http://localhost:8000/reset/"
        subject = "Password Reset Requested"
        message = render_to_string('reset.html', {
            'password_reset_link': password_reset_link,
            'username': user.first_name,
        })

        send_mail(subject, message, 'sugandhibansal26@gmail.com', [email])
        return Response({"message": "Password reset link sent."}, status=200)
    
    except Exception as e:
        return Response({
            "error": str(e)
        })

@api_view(['POST'])
def reset(request):
    try:
        
        email = request.data.get('email')
        new_password = request.data.get('password')
        if not email :
            return Response({
                "email":"Please enter valid email"
            })
        user = User.objects.get(email=email) 
        user.set_password(new_password) 
        user.save()  
        return Response({'message': 'Password updated successfully'})
    except Exception as e:
        return Response({
            'error': e
        })





# gives the list of rooms
@api_view(['GET'])
def availrooms(request):
    try:
        hotel = Hotel.objects.get(hotel_id=1)
        rooms = hotel.rooms.all()
        print(rooms)
        if rooms.exists():
            serializer = RoomSerializer(rooms,many=True)
            return Response(serializer.data)
        return Response({
            "msg":"NO rooms are there"
        })
    except Exception as e:
        return Response({
            "msg":str(e)
        })
    


#  to book a room 
@api_view(['POST'])
def bookRoom(request,hotel_id):
    try:
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "msg":str(e)
        })
    