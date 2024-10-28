from django.urls import path
from .views import home,availrooms,bookRoom,ResetPassword,reset

urlpatterns = [
    path('signup/',home,name="addding_new_user"),
    path('password/reset',ResetPassword,name="passwordReset"),
    path('reset/',reset,name="reset"),
    path("room/list",availrooms,name="availableRooms"),
    path("room/book/<int:hotel_id>",bookRoom,name="bookRoom"),
]
