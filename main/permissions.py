from rest_framework import permissions


class IsStaffDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "DELETE" and request.user.is_staff:
            return True
        return False
