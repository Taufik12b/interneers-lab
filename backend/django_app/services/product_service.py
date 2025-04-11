from django_app.repositories.product_repository import ProductRepository
from django_app.serializers.product_serializer import ProductSerializer
from django.utils import timezone


class ProductService:

    @staticmethod
    def create_product(data):
       product = ProductRepository.create(data)
       return ProductSerializer(product).data
    
    @staticmethod
    def get_all_products(ordering=None, filters=None):
        products = ProductRepository.get_all()
        if filters:
            if 'created_after' in filters:
                products = products.filter(created_at__gte=filters['created_after'])
            if 'created_before' in filters:
                products = products.filter(created_at__lte=filters['created_before'])
            if 'updated_after' in filters:
                products = products.filter(updated_at__gte=filters['updated_after'])
            if 'updated_before' in filters:
                products = products.filter(updated_at__lte=filters['updated_before'])
        if ordering:
            products = products.order_by(ordering)
        return ProductSerializer(products, many=True).data
    
    @staticmethod
    def get_product_by_id(pk):
        product = ProductRepository.get_by_id(pk)
        if not product:
            return None
        return ProductSerializer(product).data
    
    @staticmethod
    def update_product(product_data, pk):
        product = ProductRepository.get_by_id(pk)
        if not product:
            return None
        product_data["updated_at"] = timezone.now()
        updated_product = ProductRepository.update(product, product_data)
        return ProductSerializer(updated_product).data
    
    @staticmethod
    def delete_product(product_id):
        ProductRepository.delete(product_id)