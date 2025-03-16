from django.db import models
import decimal
from .mongo import db
from bson import ObjectId


class Product:
    
    collection = db['products']

    @classmethod
    def create(cls, data):
        # Convert Decimal to float if necessary
        if 'price' in data and isinstance(data['price'], decimal.Decimal):
            data['price'] = float(data['price'])
        return cls.collection.insert_one(data).inserted_id

    @classmethod
    def get_all(cls):
        return list(cls.collection.find({}))

    @classmethod
    def get_by_id(cls, product_id):
        return cls.collection.find_one({"_id": ObjectId(product_id)})

    @staticmethod
    def get_by_name(name):
        """Check if a product with the given name exists."""
        return db.products.find_one({"name": name})  # Query MongoDB for the product name
    
    @classmethod
    def update(cls, product_id, data):
        if 'price' in data and isinstance(data['price'], decimal.Decimal):
            data['price'] = float(data['price'])
        return cls.collection.update_one({"_id": ObjectId(product_id)}, {"$set": data})

    @classmethod
    def delete(cls, product_id):
        return cls.collection.delete_one({"_id": ObjectId(product_id)})
    
