from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from .models import Order
from rest_framework.response import Response
from rest_framework import status
from .serializers.OrderSerializer import OrderSerializer
from .serializers.NewOrderSerializer import OrderCreationSerializer
from .services.OrderProcessingService import OrderProcessingService
from .services.OrderCancellationService import OrderCancellationService


class OrderListView(APIView):
    """
        List all orders, or create a new order.
    """

    # List all orders in the DB
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderCreationSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = OrderProcessingService.process_order(
                serializer.validated_data
            )

            response = OrderSerializer(order)

            return Response(
                response.data,
                status=status.HTTP_201_CREATED
            )

        except ValueError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        order_id = request.query_params.get('order_id')
        OrderCancellationService.cancel_order(
            order_id=order_id
        )

        return Response(status=status.HTTP_200_OK)




