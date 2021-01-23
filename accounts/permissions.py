from rest_framework import permissions


class OwnerReadOnlyAdminEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj.user == request.user:
            return True

        return request.user.is_admin


class CustomAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # TODO the is_admin may have to change names
        return bool(request.user and request.user.is_admin)


class IsOwnerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_owner)
