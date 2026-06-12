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

from config.security.permissions import IsUser, IsAdmin

import logging

logger = logging.getLogger("app_logger")


class OrderListView(APIView):
    """
        List all orders, or create a new order.
    """

    permission_classes = [IsUser, IsAdmin]

    # List all orders in the DB
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        # Extract the user email
        user_email = request.user.email

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
                serializer.validated_data,
                user_email=user_email
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
        try:
            order_id = request.query_params.get('order_id')
            logger.info("Incoming request/...")
            OrderCancellationService.cancel_order(
                order_id=order_id
            )

            return Response(status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                data={
                    "error" : e.__str__()
                },
                status=status.HTTP_400_BAD_REQUEST
            )




