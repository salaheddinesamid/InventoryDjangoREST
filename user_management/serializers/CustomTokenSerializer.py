from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)


class CustomTokenSerializer(
    TokenObtainPairSerializer
):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        token['roles'] = list(
            user.roles.values_list(
                'role_name',
                flat=True
            )
        )

        return token
