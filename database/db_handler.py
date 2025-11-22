import os
from pymongo import MongoClient
from datetime import datetime
from config import Config

# ✅ FIX 1: Global Variable जो DB instance को रखेगा (Singleton)
_db_instance = None

def get_db_instance():
    """Returns the globally initialized DBHandler instance."""
    global _db_instance
    if _db_instance is None:
        # अगर instance मौजूद नहीं है, तो नया बनाएं और कनेक्ट करें
        _db_instance = DBHandler()
        _db_instance.connect() 
    return _db_instance

class DBHandler:
    def __init__(self):
        # ✅ FIX 2: Connection को __init__ से हटाएं
        self.client = None
        self.db = None
        self.users = None

    def connect(self):
        """Initializes the MongoDB connection using Config.MONGO_URI."""
        if self.client is None:
            # Connection को connect() method में डालें
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client["MovieBotDB"]
            self.users = self.db["users"]

    def add_new_user(self, user_id: int, username: str, first_name: str):
        if not self.users.find_one({"_id": user_id}):
            data = {
                "_id": user_id,
                "username": username,
                "first_name": first_name,
                "first_joined": datetime.utcnow(),
                "is_admin": False,
            }
            self.users.insert_one(data)
            return True
        return False

    def set_admin(self, user_id: int, value: bool = True):
        self.users.update_one({"_id": user_id}, {"$set": {"is_admin": value}}, upsert=True)

    def is_admin(self, user_id: int) -> bool:
        user = self.users.find_one({"_id": user_id})
        return bool(user and user.get("is_admin"))

# 🛑 NOTE: फ़ाइल के अंत में 'db = DBHandler()' लाइन को हटा दें (अगर मौजूद हो)।
