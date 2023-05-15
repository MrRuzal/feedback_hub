from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Разрешает доступ только пользователям с ролью администратора."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """
    Разрешение на запись доступно только для администраторов,
    для чтения - для всех.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_staff or request.user.is_admin)
        )


class IsAdminAuthorModeratorOrReadOnly(BasePermission):
    """
    Проверка, является ли пользователь администратором,
    автором или модератором или только чтение.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (not request.user.is_authenticated)
            or (
                request.user.is_admin
                or request.user.is_moredator
                or obj.author == request.user
            )
        )
