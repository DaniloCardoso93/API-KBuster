from rest_framework import permissions
from rest_framework.views import Request, View
from .models import User


class IsAdmOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_employee
        )


class IdAdmOrLoginUserOrAuthentication(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        return request.user.id == obj.id or request.user.is_employee
