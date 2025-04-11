from rest_framework import viewsets, status, pagination
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from bson import ObjectId
from django_app.serializers.product_serializer import ProductSerializer
from django_app.models.product import Product

class ProductPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

class ProductViewSet(viewsets.ViewSet):

    pagination_class = ProductPagination

    def create(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                product = Product(**serializer.validated_data)
                product.save()
                return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
            return Response(
                {"error": "Validation error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ParseError as e:
            return Response(
                {"error": "Invalid JSON format", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        try:
            products = Product.objects.all()
            paginator = self.pagination_class()
            page_size = request.query_params.get('page_size', paginator.page_size)
            try:
                page_size = int(page_size)
                if page_size > paginator.max_page_size:
                    return Response(
                        {
                            "error": "Invalid page size",
                            "message": f"Page size cannot exceed {paginator.max_page_size}."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {"error": "Invalid page size", "message": "Page size must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            paginated_products = paginator.paginate_queryset(products, request)
            serialized = ProductSerializer(paginated_products, many=True)
            return paginator.get_paginated_response(serialized.data)
        except NotFound:
            return Response(
                {"error": "Invalid page", "message": "Requested page is out of range."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        try:
            if not ObjectId.is_valid(pk):
                return Response(
                    {"error": "Invalid product ID", "message": "Product ID must be a 24-character hex string."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            product = Product.objects(id=ObjectId(pk)).first()
            if not product:
                return Response(
                    {"error": "Product not found", "message": f"No product found with ID {pk}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        except NotFound:
            return Response(
                {"error": "Invalid page", "message": "Requested page is out of range."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None):
        try:
            if not ObjectId.is_valid(pk):
                return Response(
                    {"error": "Invalid product ID", "message": "Product ID must be a 24-character hex string."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            product = Product.objects(id=ObjectId(pk)).first()
            if not product:
                return Response(
                    {"error": "Product not found", "message": f"No product found with ID {pk}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = ProductSerializer(instance=product, data=request.data)
            if serializer.is_valid():
                for field, value in serializer.validated_data.items():
                    setattr(product, field, value)

                product.save()
                return Response(
                    {
                        "message": "Product updated successfully",
                        "updated_product": ProductSerializer(product).data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Validation error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ParseError as e:
            return Response(
                {"error": "Invalid JSON format", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        try:
            if not ObjectId.is_valid(pk):
                return Response(
                    {"error": "Invalid product ID", "message": "Product ID must be a 24-character hex string."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            product = Product.objects(id=ObjectId(pk)).first()
            if not product:
                return Response(
                    {"error": "Product not found", "message": f"No product found with ID {pk}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            product_name = product.name
            product.delete()
            return Response(
                {"message": f"Product '{product_name}' deleted successfully"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
