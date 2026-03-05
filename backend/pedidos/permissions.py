from rest_framework.permissions import BasePermission, AllowAny

class PermitirTodo(BasePermission):
    def has_permission(self, request, view):
        return True
