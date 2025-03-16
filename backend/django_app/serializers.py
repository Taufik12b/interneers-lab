from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(max_length=1000, required=True)
    category = serializers.CharField(max_length=100, required=True)
    price = serializers.FloatField(min_value=0.01, required=True)
    brand = serializers.CharField(max_length=100, required=True)
    quantity = serializers.IntegerField(min_value=0, required=True)

    def validate_name(self, value):
        """Ensure the product name is unique."""
        if Product.get_by_name(value):  # Check if name exists in MongoDB
            raise serializers.ValidationError("A product with this name already exists.")
        return value
