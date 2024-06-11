from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedReadOnlyAdminAll(BasePermission):
    def has_permission(self, request, view):
        if request.user and not request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
        elif request.user.is_authenticated and request.user.is_staff:
            return True
        return False
