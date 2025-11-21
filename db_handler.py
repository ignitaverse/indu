import os
from pymongo import MongoClient
from datetime import datetime
from config import Config

class DBHandler:
    def __init__(self):
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
