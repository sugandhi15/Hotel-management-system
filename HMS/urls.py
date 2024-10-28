from django.urls import path
from .views import home

urlpatterns = [
    path('signup/',home,name="addding_new_user"),
]
