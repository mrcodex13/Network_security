import os
import pymongo
import certifi
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGODB_URI")

print("URI loaded:", MONGO_DB_URL is not None)

client = pymongo.MongoClient(
    MONGO_DB_URL,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000
)

try:
    client.admin.command("ping")
    print("✅ MongoDB connection successful")

except Exception as e:
    print("❌ MongoDB connection failed")
    print(e)