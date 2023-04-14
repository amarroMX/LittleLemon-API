from rest_framework.permissions import BasePermission, SAFE_METHODS


class EditDeleteOnlyManagerOrAdmin(BasePermission):
    message = "only manager or admin can add, update and delete menu item"

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.method in SAFE_METHODS:
            return True
        elif request.user.groups.filter(name="Manager").exists():
            return True
        else:
            return False


class UserAllOnlyManagerOrAdmin(BasePermission):
    message = "only manager can view, assign or remove user and group"

    def has_permission(self, request, view):
        group = request.user.groups.filter(name="Manager").exists()

        if request.user.is_superuser or group:
            return True
        else:
            return False
