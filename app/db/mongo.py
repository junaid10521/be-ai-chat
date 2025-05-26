import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read from .env
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB")

# Mongo connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
