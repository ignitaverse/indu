# db_handler.py (Updated Code)
import os
from pymongo import MongoClient
from datetime import datetime
from config import Config

# DBHandler अब global DB connection नहीं बनाएगा
class DBHandler:
    def __init__(self):
        # Initial client object को None पर सेट करें
        self.client = None
        self.db = None
        self.users = None

    def connect(self):
        """Initializes the MongoDB connection using Config.MONGO_URI."""
        if not self.client:
            # केवल तभी कनेक्ट करें जब Config validation हो चुकी हो
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client["MovieBotDB"]
            self.users = self.db["users"]
            
    # बाकी सारे functions (add_new_user, set_admin, is_admin) ज्यों के त्यों रहेंगे

# DBHandler का global instance (पर अभी कनेक्ट नहीं हुआ है)
db = DBHandler()
