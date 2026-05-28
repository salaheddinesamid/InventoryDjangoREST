from rest_framework import serializers
from ..models import Product


class ProductSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data.get('price', 0) < 0:
            raise serializers.ValidationError(
                "Price cannot be negative"
            )

        return data

    class Meta:
        model = Product
        fields = '__all__'
