from ..models import User, Role
from ..exceptions.UserAlreadyExistsException import UserAlreadyExistsException


class AuthenticationService:

    @staticmethod
    def authenticate():
        pass

    @staticmethod
    def register(validate_data):
        user_exists = User.objects.filter(email=validate_data['email'])

        # Create new user:
        new_user = User.objects.create(
            first_name=validate_data['first_name'],
            last_name=validate_data['last_name'],
            email=validate_data['email']
        )

        # Fetch the roles:
        role_names = validate_data['roles']
        for name in role_names:
            role = Role.objects.get(
                role_name=name
            )

            new_user.roles.add(role.id)

        new_user.set_password(
            validate_data['password']
        )

        # Save the user in the database
        new_user.save()

        return new_user
