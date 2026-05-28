from rest_framework import serializers
from ..models import User


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True)
    roles = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False
    )

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists")

        return data
