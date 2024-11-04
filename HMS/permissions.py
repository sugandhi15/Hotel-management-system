from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.account_type == 'Customer'

class IsManager(BasePermission):
    def has_permission(self,request,view):
        return request.user.account_type == 'Hotel Manager'
    
class IsAdmin(BasePermission):
    def has_permission(self,request,view):
        return request.user.account_type == 'Admin'