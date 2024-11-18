from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
DB_NAME = "fastapicluster"  
MONGO_URI = os.getenv("DB_URI", "mongodb://localhost:27017")

# Ensure MONGO_URI is set
if not MONGO_URI:
    raise ValueError("Database URI (DB_URI) is not set in the environment variables.")

# Lazy DB client initialization
_client = None

def get_db_client():
    """
    Lazily initializes and returns the MongoDB client.
    """
    global _client
    if _client is None:
        try:
            
            _client = AsyncIOMotorClient(MONGO_URI)
            
        except Exception as e:
            logging.error(f"Failed to initialize MongoDB client: {e}")
            raise
    return _client

def get_database():
    """
    Returns the MongoDB database instance.
    """
    client = get_db_client()
    db = client[DB_NAME]
    
    return db


db = get_database()





