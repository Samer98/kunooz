from rest_framework import permissions
class IsConsultant(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if str(request.user.role) == "Consultant":
            return True


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if str(request.user.role) == "Owner":
            return True

class IsWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if str(request.user.role) == "Worker":
            return True

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if str(request.user.role) == "User":
            return True

# class IsUser_Worker_Owner(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         if str(request.user.role) == "User":
#             return True