import os
from pymongo import MongoClient
from datetime import datetime
from config import Config

class DBHandler:
    def __init__(self):
        # ✅ FIX 1: Connection को __init__ से हटाएं। सिर्फ़ variables को None पर सेट करें।
        self.client = None
        self.db = None
        self.users = None

    def connect(self):
        """Initializes the MongoDB connection using Config.MONGO_URI."""
        if self.client is None:
            # ✅ FIX 2: Connection को connect() method में डालें।
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client["MovieBotDB"]
            self.users = self.db["users"]

    # आपके अन्य functions (add_new_user, set_admin, is_admin) ज्यों के त्यों रहेंगे...
    
# 🛑 NOTE: इस फ़ाइल के अंत में 'db = DBHandler()' लाइन को पूरी तरह से हटा दें।
