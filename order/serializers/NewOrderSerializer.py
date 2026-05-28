from rest_framework import serializers


#
class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


#
class OrderCreationSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(
        many=True
    )

    def validate_items(self, value):
        if len(value) == 0:
            raise serializers.ValidationError(
                "Order must contain at least one item"
            )

        return value
