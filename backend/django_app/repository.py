from .mongo import db
from decimal import Decimal
from bson import ObjectId

class ProductRepository:
    # Reference to the 'products' collection in the MongoDB database
    collection = db['products']

    @classmethod
    def get_all(cls):
        # Fetch all products from the collection
        return list(cls.collection.find({}))

    @classmethod
    def create(cls, data):
        # Convert Decimal price to float for MongoDB storage
        if 'price' in data and isinstance(data['price'], Decimal):
            data['price'] = float(data['price'])
        # Insert new product into the collection and return the inserted ID
        return cls.collection.insert_one(data).inserted_id

    @classmethod
    def get_by_id(cls, product_id):
        # Fetch a product by its unique ObjectId
        return cls.collection.find_one({"_id": ObjectId(product_id)})

    @classmethod
    def update(cls, product_id, data):
        # Convert Decimal price to float for MongoDB storage
        if 'price' in data and isinstance(data['price'], Decimal):
            data['price'] = float(data['price'])
        # Update the product with the specified ID
        return cls.collection.update_one({"_id": ObjectId(product_id)}, {"$set": data})

    @classmethod
    def delete(cls, product_id):
        # Delete the product with the specified ID
        return cls.collection.delete_one({"_id": ObjectId(product_id)})

    @classmethod
    def get_by_name(cls, name):
        # Fetch a product by its name
        return cls.collection.find_one({"name": name})
