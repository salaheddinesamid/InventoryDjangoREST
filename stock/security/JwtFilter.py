from rest_framework.permissions import BasePermission


class HasRole(BasePermission):

    allowed_roles = []

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        user_roles = request.user.roles.values_list(
            'name',
            flat=True
        )

        return any(role in user_roles for role in self.allowed_roles)


class IsAdmin(HasRole):
    allowed_roles = ['ADMIN']


class IsUser(HasRole):
    allowed_roles = ['User']


class IsAdminOrUser(HasRole):
    allowed_roles = ['ADMIN', 'USER']