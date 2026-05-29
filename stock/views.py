from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

# Create your views here.


"""

"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers.ProductSerializer import ProductSerializer
from .services.StockUpdateService import StockUpdateService
from .services.ProductAdderService import ProductAdderService
from .services.ProductRemoveService import ProductRemoveService
from config.security.permissions import IsAdmin, IsAdminOrUser
import logging

logger = logging.getLogger("app_logger")


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductList(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination


class ProductListView(APIView):
    pagination_class = LargeResultsSetPagination

    def get_permissions(self):

        if self.request.method == "GET":
            permission_classes = []
        if self.request.method == "POST":
            permission_classes = [IsAdmin]

        return [
            permission()
            for permission in permission_classes
        ]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            new_product = ProductAdderService.add_product(serializer.validated_data)
            res_data = ProductSerializer(new_product)
            return Response(data=res_data.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProductDetailView(APIView):

    def get_object(self, request):
        product_name = request.query_params.get('name')
        return Product.objects.get(name=product_name)

    def get(self, request):
        try:
            product = self.get_object(request)
            serializer = ProductSerializer(product)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request):
        product_id = request.query_params.get('product_id')
        serializer = ProductSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            updated_product = StockUpdateService.update_product(
                product_id=product_id,
                validated_data=serializer.validated_data
            )

            response_body = ProductSerializer(updated_product)
            return Response(data=response_body.data, status=status.HTTP_200_OK)

        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):

        product_id = request.query_params.get('product_id')
        try:
            ProductRemoveService.remove_product(product_id)
            return Response(status=status.HTTP_200_OK)
        except Product.DoesNotExist():
            return Response(status=status.HTTP_404_NOT_FOUND)
