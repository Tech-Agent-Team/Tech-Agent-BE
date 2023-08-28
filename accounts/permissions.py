from rest_framework.permissions import BasePermission,IsAdminUser

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_customer)

class IsTechnicianUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_technician)
    