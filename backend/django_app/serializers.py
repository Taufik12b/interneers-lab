from rest_framework import serializers
from .repository import ProductRepository


class ProductSerializer(serializers.Serializer):

    id = serializers.CharField(read_only=True)
    name = serializers.CharField(
        max_length=255,
        required=True,
        error_messages={
            'blank': 'Product name cannot be empty.',
            'max_length': 'Product name cannot exceed 255 characters.'
        }
    )
    description = serializers.CharField(
        max_length=1000,
        required=True,
        error_messages={
            'blank': 'Description cannot be empty.',
            'max_length': 'Description cannot exceed 1000 characters.'
        }
    )
    category = serializers.CharField(
        max_length=100,
        required=True,
        error_messages={
            'blank': 'Category cannot be empty.',
            'max_length': 'Category cannot exceed 100 characters.'
        }
    )
    price = serializers.FloatField(
        min_value=0.01,
        required=True,
        error_messages={
            'invalid': 'Price must be a valid number.',
            'min_value': 'Price must be greater than zero.'
        }
    )
    brand = serializers.CharField(
        max_length=100,
        required=True,
        error_messages={
            'blank': 'Brand cannot be empty.',
            'max_length': 'Brand cannot exceed 100 characters.'
        }
    )
    quantity = serializers.IntegerField(
        min_value=0,
        required=True,
        error_messages={
            'invalid': 'Quantity must be a valid integer.',
            'min_value': 'Quantity cannot be negative.'
        }
    )

    def validate_name(self, value):
        request = self.context.get('request')
        product_id = self.instance['_id'] if self.instance else None

        if request and request.method in ['POST', 'PUT']:
            existing_product = ProductRepository.get_by_name(value)
            if existing_product and str(existing_product['_id']) != str(product_id):
                raise serializers.ValidationError("A product with this name already exists.")
        return value

