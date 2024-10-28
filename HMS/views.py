# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .serializer import Userserializer,RoomSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Hotel

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def home(request):
    serializer = Userserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def availrooms(request):
    try:
        hotel = Hotel.objects.get(id=1)
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
    