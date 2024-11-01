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
from .models import Hotel,Room,Booking
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator







@csrf_exempt
#  to register a new user
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def availrooms(request):
    try:
        hotel = Hotel.objects.get(hotel_id=1)
        rooms = hotel.rooms.all()
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
    




#  to book a room accessible to customer
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookRoom(request,hotel_id):
    try:
        email = request.user.email
        user = User.objects.get(email = email)
        if user.account_type == "Customer":
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "msg":"Sorry, U can not access this page"
        })
    except Exception as e:
        return Response({
            "msg":str(e)
        })
    





# to update the room accesible to hotel manager
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateRoom(request,room_id):
    try:
        data = request.data 
        if not data :
             return Response({
                 "msg":"Please enter data"
             })
        email = request.user.email
        user = User.objects.get(email = email)
        if user.account_type == "Hotel Manager":
            room_info = Room.objects.get(room_no = room_id)
            serializer = RoomSerializer(room_info,data = request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({
                "msg":"Please enter valid data"
            })
        return Response({
            "msg":"Sorry, U can not access this page"
        })
    except Exception as e:
        return Response({
            "msg":str(e)
        })
    






# to checkout from a room
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    try:
        room_id = request.data.get('room_id')
        email = request.user.email
        user = User.objects.get(email = email)
        if user.account_type == "Hotel Manager":
            curr_room = Room.objects.get(room_no = room_id)
            data = {
                "availability" : "Available"
            }
            serializer = RoomSerializer(curr_room,data=data,partial = True)
            if serializer.is_valid():
                serializer.save()
            Booking.objects.get(room = room_id).delete()
            return Response({
                "msg":"You successfully Checkout",
                "room_no":room_id
            })
        return Response({
            "msg":"Sorry, U can not access this page"
        })
    except Exception as e:
        return Response({
            "msg":str(e)
        })








# to get all the bookings for a customer
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listBookings(request):
    try:
        email = request.user.email
        user = User.objects.get(email = email)
        book = user.bookings.all()
        if book.exists():
            serializer = BookingSerializer(book,many=True)
            return Response(serializer.data)
        return Response({
            "msg":"NO bookings are there"
        })
    except Exception as e:
        return Response({
            "msg":str(e)
        })







#  to get all the bookings
@api_view(['GET'])
def bookingsList(request):
    try:
        email = request.user.email
        user = User.objects.get(email = email)
        if user.account_type == "Hotel Manager":
            booking = Booking.objects.all()
            if booking.exists():
                serializer = BookingSerializer(booking,many=True)
                return Response(serializer.data)
            return Response({
                "msg":"NO bookings are there"
            })
        return Response({
            "msg":"Sorry, U can not access this page"
        })
    except Exception as e:
        return Response({
            "msg":str(e)
        })
    






# to cancel all the bookings by a user
@api_view(['DELETE'])
def cancelBooking(request):
    try:
        email = request.user.email
        user = User.objects.get(email = email)
        if user.account_type == "Hotel Manager":
            user.bookings.all().delete()
            return Response({
                "msg":"canceled the booking successfully"
            })
        return Response({
            "msg":"Sorry, U can not access this page"
        })
    except Exception as e:
        return Response({
            "msg":str(e)
        })
    






# to delete a user 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request):
    try:
        email1 = request.query_params.get('email')
        if not email1:
            return Response({"msg": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        email2 = request.user.email
        user = User.objects.get(email = email2)
        user.is_superuser = True
        if user.account_type == "Admin":
            User.objects.get(email=email1).delete()
            return Response({
                "msg":"user deleted successfully"
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "msg":"Sorry, U can not access this page"
        })
    except Exception as e:
        return Response({
            "msg":str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    







#  to get list of all the users
@api_view(['GET'])
def availusers(request):
    try:
        user = User.objects.all()
        serializer = Userserializer(user,many=True)
        return Response(serializer.data)
    except Exception as e :
        return Response({
            "msg":str(e)
        })

