from rest_framework import permissions
class IsConsultant(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if str(request.user.role) == "Consultant":
            return True