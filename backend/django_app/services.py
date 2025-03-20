from .repository import ProductRepository

class ProductService:

    @staticmethod
    def get_all_products():
        # Fetch all products from the repository
        products = ProductRepository.get_all()
        # Convert ObjectId to string for better readability and JSON compatibility
        for product in products:
            product['_id'] = str(product['_id'])
        return products
    
    @staticmethod
    def create_product(data):
        # Create a new product and return its ID as a string
        product_id = ProductRepository.create(data)
        return str(product_id)

    @staticmethod
    def get_product_by_id(product_id):
        # Fetch a product by its ID
        product = ProductRepository.get_by_id(product_id) 
        if product:
            # Convert ObjectId to string
            product['_id'] = str(product['_id'])
        return product

    @staticmethod
    def update_product(product_id, data):
        # Update product details based on product ID
        result = ProductRepository.update(product_id, data)
        return result

    @staticmethod
    def delete_product(product_id):
        # Delete a product by its ID
        result = ProductRepository.delete(product_id)
        return result
