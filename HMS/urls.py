from django.urls import path
from .views import signup,availrooms,bookRoom,ResetPassword,reset,setPassword,updateRoom,checkout,listBookings,bookingsList,cancelBooking,availusers,welcome,deleteUser
from rest_framework_simplejwt.views import  TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('signup/',signup.as_view(),name="addding_new_user"),
    path('login',  TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
    path('password/reset',ResetPassword.as_view(),name="passwordReset"),
    path('reset/',reset.as_view(),name="reset"),
    path('password/reset/<str:token>',setPassword.as_view(),name="setPassword"),
    path("room/list",availrooms.as_view(),name="availableRooms"),
    path("room/book",bookRoom.as_view(),name="bookRoom"),
    path("room/update/<int:room_id>",updateRoom.as_view(),name="updateRoom"),
    path("room/checkout",checkout.as_view(),name="checkout"),
    path("booking/list",listBookings.as_view(),name="listBookings"),
    path("booking/all",bookingsList.as_view(),name="bookingsList"),
    path("booking/cancel",cancelBooking.as_view(),name="cancelBooking"),
    path("delete",deleteUser.as_view(),name="deleteUser"),
    path("users",availusers.as_view(),name="users"), #to check users
    path("welcome",welcome.as_view()), # to redirect after oauth 
]
