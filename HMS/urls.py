from django.urls import path
from .views import home,availrooms

urlpatterns = [
    path('signup/',home,name="addding_new_user"),
    path("room/list",availrooms,name="availableRooms")
]
