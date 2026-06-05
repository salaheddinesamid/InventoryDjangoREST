from rest_framework import serializers


# JSON serializer for order item
class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


# JSON serializer for order details
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
