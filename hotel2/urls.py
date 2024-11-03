from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import  TokenRefreshView
from HMS.views import deleteUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
    path('',include('HMS.urls')),
    path("delete",deleteUser,name="deleteUser"),
    path('accounts/', include('allauth.urls')),
]
