from django.urls import path
from .views import home,availrooms,bookRoom,ResetPassword,reset,setPassword,updateRoom,checkout,listBookings,bookingsList,cancelBooking,availusers

urlpatterns = [
    path('signup/',home,name="addding_new_user"),
    path('password/reset',ResetPassword,name="passwordReset"),
    path('reset/',reset,name="reset"),
    path('password/reset/<str:token>',setPassword,name="setPassword"),
    path("room/list",availrooms,name="availableRooms"),
    path("room/book/<int:hotel_id>",bookRoom,name="bookRoom"),
    path("room/update/<int:room_id>",updateRoom,name="updateRoom"),
    path("room/checkout",checkout,name="checkout"),
    path("booking/list",listBookings,name="listBookings"),
    path("booking/all",bookingsList,name="bookingsList"),
    path("booking/cancel",cancelBooking,name="cancelBooking"),
    path("users",availusers,name="users"),
]
