from rest_framework.permissions import BasePermission


class HasRole(BasePermission):

    allowed_roles = []

    def has_permission(self, request, view):

        # If the HTTP request does not have any authentication
        if not request.user.is_authenticated:
            return False

        # Extract use roles and authorities from the HTTP request
        user_roles = request.user.roles.values_list(
            'name',
            flat=True
        )

        # Return if the user has at least of the allowed roles
        return any(role in user_roles for role in self.allowed_roles)


class IsAdmin(HasRole):
    allowed_roles = ['ADMIN']


class IsUser(HasRole):
    allowed_roles = ['User']


class IsAdminOrUser(HasRole):
    allowed_roles = ['ADMIN', 'USER']