from rest_framework import viewsets, status
from .services import ProductService
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, NotFound
import json
from json.decoder import JSONDecodeError
from .serializers import ProductSerializer
from bson.errors import InvalidId


class ProductViewSet(viewsets.ViewSet):

    # GET /products/ - List all products with pagination
    def list(self, request):
        try:
            products = ProductService.get_all_products()
            if not products:
                # Return 404 if no products are found
                return Response(
                    {"error": "No products found", "details": "There are no products available at the moment."},
                    status=status.HTTP_404_NOT_FOUND
                )
            paginator = PageNumberPagination()
            try:
                # Apply pagination to the product list
                paginated_products = paginator.paginate_queryset(products, request)
            except NotFound:
                # Handle invalid page number
                return Response(
                    {"error": "Invalid page number", "details": "The requested page number exceeds the available pages."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Return paginated response
            return paginator.get_paginated_response(paginated_products)
        except Exception as e:
            # Handle unexpected server errors
            return Response(
                {"error": "Failed to fetch products", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # POST /products/ - Create a new product
    def create(self, request):
        try:
            # Decode and parse the JSON body
            data = json.loads(request.body.decode('utf-8'))
        except JSONDecodeError as e:
            # Handle invalid JSON format
            return Response(
                {"error": "Invalid JSON format", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Validate data using serializer
        serializer = ProductSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            # Save the product if data is valid
            product_id = ProductService.create_product(serializer.validated_data)
            return Response(
                {'id': product_id}, 
                status=status.HTTP_201_CREATED
            )
        # Return validation errors if invalid data
        return Response(
            {'error': 'Invalid product data', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    # GET /products/{id}/ - Retrieve a specific product by ID
    def retrieve(self, request, pk=None):
        try: 
            product = ProductService.get_product_by_id(pk)
            if product:
                product['_id'] = str(product['_id'])  # Convert ObjectId to string
                return Response(product)
            # Return 404 if product is not found
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except InvalidId:
            # Handle invalid ObjectId format
            return Response(
                {'error': 'Invalid product ID format'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # PUT /products/{id}/ - Update an existing product by ID
    def update(self, request, pk=None):
        try:
            # Decode and parse the JSON body
            data = json.loads(request.body.decode('utf-8'))
        except JSONDecodeError as e:
            # Handle invalid JSON format
            return Response(
                {"error": "Invalid JSON format", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Check if the product exists
            product_instance = ProductService.get_product_by_id(pk)
            if not product_instance:
                return Response(
                    {'error': 'Product not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            # Validate and update product using serializer
            serializer = ProductSerializer(instance=product_instance, data=data, context={'request': request})
            if serializer.is_valid():
                result = ProductService.update_product(pk, serializer.validated_data)
                if result.matched_count == 0: 
                    # If no product matched the given ID
                    return Response(
                        {'error': 'Product not found'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                if result.modified_count == 0: 
                    # If no changes were made
                    return Response(
                        {'message': 'No changes detected'}, 
                        status=status.HTTP_200_OK
                    )
                # Return success response if update is successful
                return Response(
                    {'message': 'Product updated'}, 
                    status=status.HTTP_200_OK
                )
            # Return validation errors if data is invalid
            return Response(
                {'error': 'Invalid product data', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except InvalidId:
            # Handle invalid ObjectId format
            return Response(
                {'error': 'Invalid product ID format'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    # DELETE /products/{id}/ - Delete a product by ID
    def destroy(self, request, pk=None):
        try:
            # Attempt to delete the product
            result = ProductService.delete_product(pk)
            if result.deleted_count:
                # If deletion is successful
                return Response(
                    {'message': 'Product deleted'}, 
                    status=status.HTTP_204_NO_CONTENT
                )
            # If product not found
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except InvalidId:
            # Handle invalid ObjectId format
            return Response(
                {'error': 'Invalid product ID format'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
