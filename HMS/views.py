from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializer import Userserializer,RoomSerializer,BookingSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Hotel,Room,Booking
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from .permissions import IsCustomer,IsManager,IsAdmin
from .forms import SignupForm





# signup page with recapcha
def signup(request): 
    if request.method == 'POST': 
        form = SignupForm(request.POST) 
        data = {
            "email" : request.POST.get('email'),
            "first_name" : request.POST.get('first_name'),
            "last_name" : request.POST.get('last_name'),
            "password" : request.POST.get('password'),
            "account_type" : request.POST.get('account_type')
        }
        serializer = Userserializer(data=data)
        if form.is_valid():
            if serializer.is_valid():
                try:
                    serializer.save()
                    return HttpResponse("You have signed up") 
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse("Please enter valid data")
        else:
            return HttpResponse("OOPS! Bot suspected.") 
            
    else: 
        form = SignupForm() 
          
    return render(request, 'signup.html', {'form':form})



#  to register a new user
'''
class signup(APIView):
    permission_classes = (AllowAny,)

    def get(request):
        form = SignupForm()
        return render(request, 'signup.html', {'form':form})

    def post(self,request):
        try:
            serializer = Userserializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "msg": "Signed up successfully"
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "msg":"error occured"
                })
            
        except Exception as e:
            return Response({
                "msg":"Internal server error"
            })
'''      







#  to reset password without token
class ResetPassword(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
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
                "error": "Internal server error"
            })







# link sent on mail to reseet password
class reset(APIView):

    def post(self,request):
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
                'error': "Internal server error"
            })







#  link on mail to set the password using token
class setPassword(APIView):

    def post(self,request,token):
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
                "msg":"Internal server error"
            })
    






# gives the list of rooms
class availrooms(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            rooms = Room.objects.all()
            if rooms.exists():
                serializer = RoomSerializer(rooms,many=True)
                return Response(serializer.data)
            return Response({
                "msg":"NO rooms are there"
            })
        except Exception as e:
            return Response({
                "msg":"Internal server error"
            })
        





#  to book a room accessible to customer
class bookRoom(APIView):
    permission_classes = ( IsAuthenticated ,IsCustomer)

    def post(self,request):
        try:
            hotel_id  = request.query_params.get('hotel_id')
            email = request.user.email
            user = User.objects.get(email = email)
            if user.account_type == "Customer":
                serializer = BookingSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    #  email to manager 
                    subject1 = "New Booking Alert"
                    manager_email='sugandhibansal26@gmail.com'
                    message1 = (
                        f"Hello Manager,\n\n"
                        f"A new booking has been made with the following details:\n"
                        f"Check-in Date: {serializer.validated_data['check_in_date']}\n"
                        f"Check-out Date: {serializer.validated_data['check_out_date']}\n\n"
                    )
                    send_mail(subject1, message1, "sugandhibansal26@gmail.com", [manager_email])
                    # email to customer
                    subject = "Confirm your room booking"
                    message = (
                            f"Dear Customer,\n\n"
                            f"You have made a booking for hotel room. Here are your booking details:\n"
                            f"Check-in Date: {serializer.validated_data['check_in_date']}\n"
                            f"Check-out Date: {serializer.validated_data['check_out_date']}\n\n"
                            f"Thank you"
                        )
                    send_mail(subject, message, 'sugandhibansal26@gmail.com', [email])
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "msg":"Sorry, U can not access this page"
            })
        except Exception as e:
            return Response({
                "msg":"Internal server error"
            })
    





# to update the room accesible to hotel manager
class updateRoom(APIView):
    permission_classes = (IsAuthenticated , IsManager)

    def put(request,room_id):
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
                "msg":"Internal server error"
            })
        






# to checkout from a room
class checkout(APIView):
    permission_classes = (IsAuthenticated , IsCustomer)

    def post(request):
        try:
            room_id = request.data.get('room_id')
            email = request.user.email
            user = User.objects.get(email = email)
            if user.account_type == "Customer":
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
                "msg":"Internal server error"
            })








# to get all the bookings for a customer
class listBookings(APIView):
    permission_classes=(IsAuthenticated , IsCustomer) 

    def get(self,request):
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
                "msg":"Internal server error"
            })







#  to get all the bookings for hotel manager
class bookingsList(APIView):
    permission_classes=(IsAuthenticated , IsManager)

    def get(self,request):
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
                "msg":"Internal server error"
            })
    






# to cancel all the bookings by a customer
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated , IsCustomer])
class cancelBooking(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)

    def delete(request):
        try:
            email = request.user.email
            user = User.objects.get(email = email)
            if user.account_type == "Customer":
                user.bookings.all().delete()
                return Response({
                    "msg":"canceled the booking successfully"
                })
            return Response({
                "msg":"Sorry, U can not access this page"
            })
        except Exception as e:
            return Response({
                "msg":"Internal server error"
            })
    






# to delete a user by admin
class deleteUser(APIView):
    permission_classes = (IsAuthenticated,IsAdmin)

    def delete(request):
        try:
            email1 = request.query_params.get('email')
            if not email1:
                return Response({"msg": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
            User.objects.get(email=email1).delete()
            return Response({
                "msg":"user deleted successfully"
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "msg":"Internal server error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        







#  to get list of all the users
class availusers(APIView):

    def get(self,request):
        try:
            user = User.objects.all()
            serializer = Userserializer(user,many=True)
            return Response(serializer.data)
        except Exception as e :
            return Response({
                "msg":"Internal server error"
            })






# welcome page (redirected after oauth)
class welcome(APIView):

    def get(self,request):
        try:
            return Response({
                "msg":"Hello, welcome to Hotel Management System"
            })
        except Exception as e:
            return Response({
                "msg":"Internal server error"
            })
    