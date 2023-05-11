from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Разрешает доступ только пользователям с ролью администратора."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'admin'


class IsAdminOrReadOnly(BasePermission):
    """
    Разрешение на запись доступно только для администраторов,
    для чтения - для всех.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'admin'


class IsAdminAuthorModeratorOrReadOnly(BasePermission):
    """
    Проверка, является ли пользователь администратором,
    автором или модератором или только чтение.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif (
            not request.user.is_authenticated
            or request.user.role == 'moderator'
        ):
            return False
        return request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif not request.user.is_authenticated:
            return False
        return (
            request.user.role == 'admin'
            or request.user.role == 'moderator'
            or obj.author == request.user
            or request.method in SAFE_METHODS
        )
