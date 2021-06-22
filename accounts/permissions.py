from rest_framework import permissions

from accounts.models import User
from entries.models import Entry


class ObjectOwnerReadOnlyAdminEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Entry) and not request.user.is_admin \
                and obj.user == request.user:
            if obj.comments != request.data.get('comments'):
                return True
        return bool(request.method in permissions.SAFE_METHODS
                    and obj.user == request.user) or request.user.is_admin


class ObjectOwnerOrAdminUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or bool(request.user == obj.user)


class ImageOwnerOrAdminUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or bool(request.user == obj.entry.user)


class ObjectOwnerOrSuperuserUpdate(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS) or \
               request.user.is_superuser or \
               bool(request.method != 'POST')

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
        return bool(request.user and request.user.is_admin)


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
