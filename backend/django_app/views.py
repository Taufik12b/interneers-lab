from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from bson import ObjectId


class ProductViewSet(viewsets.ViewSet):

    def list(self, request):
        products = Product.get_all()
        for product in products:
            product['_id'] = str(product['_id']) 
        return Response(products)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product_id = Product.create(serializer.validated_data)
            return Response({'id': str(product_id)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        product = Product.get_by_id(pk)
        if product:
            product['_id'] = str(product['_id'])
            return Response(product)
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            result = Product.update(pk, serializer.validated_data)
            if result.modified_count:
                return Response({'message': 'Product updated'})
            return Response({'error': 'Product not found or data unchanged'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        result = Product.delete(pk)
        if result.deleted_count:
            return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
