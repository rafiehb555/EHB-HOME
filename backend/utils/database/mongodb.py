import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from typing import Optional
from dotenv import load_dotenv

        from bson import ObjectId
        from bson import ObjectId
        from bson import ObjectId
        from bson import ObjectId



"""
MongoDB Configuration for EHB Backend
"""

load_dotenv()

# MongoDB Configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "ehb_database")

# Global MongoDB client
mongodb_client: Optional[AsyncIOMotorClient] = None
mongodb_sync_client: Optional[MongoClient] = None


async def connect_to_mongodb():
    """Connect to MongoDB"""
    global mongodb_client, mongodb_sync_client

    try:
        # Async client for FastAPI
        mongodb_client = AsyncIOMotorClient(MONGO_URL)

        # Sync client for operations that need it
        mongodb_sync_client = MongoClient(MONGO_URL)

        # Test connection
        await mongodb_client.admin.command('ping')
        print("✅ MongoDB connection successful")

        return mongodb_client
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None


async def close_mongodb_connection():
    """Close MongoDB connection"""
    global mongodb_client, mongodb_sync_client

    if mongodb_client:
        mongodb_client.close()
    if mongodb_sync_client:
        mongodb_sync_client.close()
    print("🔌 MongoDB connection closed")


def get_mongodb_client():
    """Get MongoDB client"""
    return mongodb_client


def get_mongodb_sync_client():
    """Get MongoDB sync client"""
    return mongodb_sync_client


def get_database():
    """Get database instance"""
    if mongodb_client:
        return mongodb_client[MONGO_DB_NAME]
    return None





def get_collection(collection_name: str):
    """Get collection instance"""
    db = get_database()
    if db:
        return db[collection_name]
    return None


# Database operations
async def create_user(user_data: dict):
    """Create a new user"""
    collection = get_collection("users")
    if collection:
        result = await collection.insert_one(user_data)
        return result.inserted_id
    return None


async def get_user(user_id: str):
    """Get user by ID"""
    collection = get_collection("users")
    if collection:
        user = await collection.find_one({"_id": ObjectId(user_id)})
        return user
    return None


async def get_user_by_email(email: str):
    """Get user by email"""
    collection = get_collection("users")
    if collection:
        user = await collection.find_one({"email": email})
        return user
    return None


async def update_user(user_id: str, update_data: dict):
    """Update user"""
    collection = get_collection("users")
    if collection:
        result = await collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    return False


async def create_service(service_data: dict):
    """Create a new service"""
    collection = get_collection("services")
    if collection:
        result = await collection.insert_one(service_data)
        return result.inserted_id
    return None


async def get_services():
    """Get all services"""
    collection = get_collection("services")
    if collection:
        services = await collection.find().to_list(length=None)
        return services
    return []


async def get_service(service_id: str):
    """Get service by ID"""
    collection = get_collection("services")
    if collection:
        service = await collection.find_one({"_id": ObjectId(service_id)})
        return service
    return None


async def update_service(service_id: str, update_data: dict):
    """Update service"""
    collection = get_collection("services")
    if collection:
        result = await collection.update_one(
            {"_id": ObjectId(service_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    return False


async def create_transaction(transaction_data: dict):
    """Create a new transaction"""
    collection = get_collection("transactions")
    if collection:
        result = await collection.insert_one(transaction_data)
        return result.inserted_id
    return None


async def get_transactions(user_id: str = None):
    """Get transactions"""
    collection = get_collection("transactions")
    if collection:
        if user_id:
            transactions = await collection.find({"user_id": user_id}).to_list(length=None)
        else:
            transactions = await collection.find().to_list(length=None)
        return transactions
    return []


# Initialize database with sample data
async def initialize_database():
    """Initialize database with sample data"""
    db = get_database()
    if not db:
        return

    # Check if collections exist
    collections = await db.list_collection_names()

    if "users" not in collections:
        # Create users collection with sample data
        users_data = [
            {
                "username": "admin",
                "email": "admin@ehb.com",
                "full_name": "Admin User",
                "sql_level": "High",
                "sql_points": 1000,
                "sql_rank": "Expert",
                "status": "active",
                "is_verified": True,
                "is_admin": True,
                "verification_progress": 100,
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "username": "user1",
                "email": "user1@ehb.com",
                "full_name": "Test User",
                "sql_level": "Normal",
                "sql_points": 500,
                "sql_rank": "Intermediate",
                "status": "active",
                "is_verified": True,
                "is_admin": False,
                "verification_progress": 75,
                "created_at": "2024-01-15T00:00:00Z"
            }
        ]

        users_collection = get_collection("users")
        if users_collection:
            await users_collection.insert_many(users_data)
            print("✅ Users collection initialized")

    if "services" not in collections:
        # Create services collection with sample data
        services_data = [
            {
                "name": "Personal Security System (PSS)",
                "type": "pss",
                "status": "active",
                "port": 4001,
                "host": "localhost",
                "endpoint": "/api/pss",
                "description": "Advanced personal security and verification system",
                "version": "1.0.0",
                "documentation_url": "/docs/pss",
                "is_healthy": True,
                "response_time": 150,
                "error_count": 0,
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "name": "Easy Management Office (EMO)",
                "type": "emo",
                "status": "active",
                "port": 4003,
                "host": "localhost",
                "endpoint": "/api/emo",
                "description": "Comprehensive office management solution",
                "version": "1.0.0",
                "documentation_url": "/docs/emo",
                "is_healthy": True,
                "response_time": 200,
                "error_count": 0,
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "name": "Exam Decision Registration (EDR)",
                "type": "edr",
                "status": "active",
                "port": 4002,
                "host": "localhost",
                "endpoint": "/api/edr",
                "description": "Educational examination and decision system",
                "version": "1.0.0",
                "documentation_url": "/docs/edr",
                "is_healthy": True,
                "response_time": 180,
                "error_count": 0,
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "name": "Job Profile System (JPS)",
                "type": "jps",
                "status": "active",
                "port": 4005,
                "host": "localhost",
                "endpoint": "/api/jps",
                "description": "Professional job profile and career management",
                "version": "1.0.0",
                "documentation_url": "/docs/jps",
                "is_healthy": True,
                "response_time": 120,
                "error_count": 0,
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "name": "GoSellr E-commerce",
                "type": "gosellr",
                "status": "active",
                "port": 4004,
                "host": "localhost",
                "endpoint": "/api/gosellr",
                "description": "Complete e-commerce platform for businesses",
                "version": "1.0.0",
                "documentation_url": "/docs/gosellr",
                "is_healthy": True,
                "response_time": 250,
                "error_count": 0,
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]

        services_collection = get_collection("services")
        if services_collection:
            await services_collection.insert_many(services_data)
            print("✅ Services collection initialized")

    print("✅ Database initialization complete")


# Test connection
async def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        client = await connect_to_mongodb()
        if client:
            await client.admin.command('ping')
            return True
        return False
    except Exception as e:
        print(f"❌ MongoDB connection test failed: {e}")
        return False
