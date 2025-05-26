from pymongo import MongoClient

# MongoDB connection (local)
client = MongoClient("mongodb://localhost:27017")
db = client["ai_chat"]
