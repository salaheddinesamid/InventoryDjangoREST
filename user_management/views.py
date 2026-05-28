from django.shortcuts import render
from rest_framework.views import APIView
from .services.AuthenicationService import AuthenticationService
from .serializers.RegistrationSerializer import RegistrationSerializer
from .serializers.UserSerializer import UserSerializer
from .exceptions.UserAlreadyExistsException import UserAlreadyExistsException
from rest_framework.response import Response
from .models import User
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

from .serializers.CustomTokenSerializer import CustomTokenSerializer


# Create your views here.

class AuthenticationView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class RegistrationView(APIView):

    def post(self, request):

        try:
            #
            serializer = RegistrationSerializer(data=request.data)

            # Verify if the request data is valid
            serializer.is_valid(raise_exception=True)

            new_user = AuthenticationService.register(
                validate_data=serializer.validated_data
            )

            response_serializer = UserSerializer(instance=new_user)

            return Response(
                data=response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        except UserAlreadyExistsException:
            return Response(
                data={
                    "error": "User already exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ClientListView(APIView):

    def get(self, request):

        users = User.objects.all()
        serializer = UserSerializer(
            instance=users,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )