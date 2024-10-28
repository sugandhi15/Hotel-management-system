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
from .models import Hotel,Room
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator





#  to register a new user
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def home(request):
    try:
        serializer = Userserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "msg":str(e)
        })
        



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
        token = default_token_generator.make_token(user)
        password_reset_link = "http://localhost:8000/reset/"
        password_reset_link_token = f'http://localhost:8000/password/reset/{token}'
        subject = "Password Reset Requested"
        message = render_to_string('reset.html', {
            'password_reset_link': password_reset_link,
            'password_reset_link_token':password_reset_link_token,
            'username': user.first_name,
        })

        send_mail(subject, message, 'sugandhibansal26@gmail.com', [email])
        return Response({"message": "Password reset link sent."}, status=200)
    
    except Exception as e:
        return Response({
            "error": str(e)
        })





# link sent on mail to reseet password
@api_view(['POST'])
def reset(request):
    try: 
        email = request.data.get('email')
        new_password = request.data.get('password')
        if not new_password:
            return Response({
                "password":"Please enter a password."
            })
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




#  link on mail to set the password using token
@api_view(['POST'])
def setPassword(request,token):
    try:
        new_password = request.data.get('password')
        for possible_user in User.objects.all():
            if default_token_generator.check_token(possible_user, token):
                user = possible_user
                user.set_password(new_password) 
                user.save()  
                return Response({'message': 'Password updated successfully'})
        return Response({
            "msg":"Please enter a valid token"
        })
    except Exception as e:
        return Response({
            "msg":str(e)
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
    




# to update the room
@api_view(['PUT'])
def updateRoom(request,room_id):
    try:
        data = request.data 
        if not data :
             return Response({
                 "msg":"Please enter data"
             })
        # room_no = room_id
        room_info = Room.objects.get(room_no = room_id)
        # room_type = request.data.get('room_type')
        # price = request.data.get('price')
        # availability = request.data.get('availability')
        serializer = RoomSerializer(room_info,data = request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({
            "msg":"Please enter valid data"
        })
    except Exception as e:
        return Response({
            "msg":str(e)
        })
    
    
