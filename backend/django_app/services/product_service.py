from django_app.repositories.product_repository import ProductRepository
from django_app.serializers.product_serializer import ProductSerializer


class ProductService:

    @staticmethod
    def create_product(data):
       product = ProductRepository.create(data)
       return ProductSerializer(product).data
    
    @staticmethod
    def get_all_products():
        products = ProductRepository.get_all()
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
        updated_product = ProductRepository.update(product, product_data)
        return ProductSerializer(updated_product).data
    
    @staticmethod
    def delete_product(product_id):
        ProductRepository.delete(product_id)