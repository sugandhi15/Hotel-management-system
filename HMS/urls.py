from django.urls import path
from .views import home,availrooms,bookRoom

urlpatterns = [
    path('signup/',home,name="addding_new_user"),
    path("room/list",availrooms,name="availableRooms"),
    path("room/book/<int:hotel_id>",bookRoom,name="bookRoom"),
]
