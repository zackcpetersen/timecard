from rest_framework import permissions

from accounts.models import User


class ObjectOwnerReadOnlyAdminEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.method in permissions.SAFE_METHODS
                    and obj.user == request.user) or request.user.is_admin


class ObjectOwnerOrAdminUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user) or request.user.is_admin


class ObjectOwnerOrSuperuserUpdate(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS
                    and request.user.is_admin) or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return bool(obj == request.user) or request.user.is_superuser
        return bool(obj.user == request.user) or request.user.is_superuser


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS
                    and request.user) or request.user.is_admin


class CustomAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # TODO the is_admin may have to change names
        return bool(request.user and request.user.is_admin)


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
