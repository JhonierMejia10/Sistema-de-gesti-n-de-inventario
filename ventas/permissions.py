from rest_framework.permissions import BasePermission, AllowAny, IsAdminUser

class PermitirTodo(BasePermission):
    def has_permission(self, request, view):
        return True

class PermitirAdmin(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create','destroy','update']:
            return IsAdminUser().has_permission(request, view)
        else:
            return AllowAny().has_permission(request,view)