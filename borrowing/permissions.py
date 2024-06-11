from rest_framework.permissions import BasePermission


class IsAuthenticatedEmailVerifiedReadOnlyAdminAll(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_verified == 1 and view.method in (
                "create",
                "list",
                "retrieve"
        ):
            return True
        elif request.user.is_authenticated and request.user.is_staff:
            return True
        return False
