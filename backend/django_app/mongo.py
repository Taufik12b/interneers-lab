from pymongo import MongoClient

# Create a connection to the MongoDB server running locally on port 27017
client = MongoClient('mongodb://localhost:27017/')

# Access the 'shop' database (creates it if it doesn't exist)
db = client['shop']
