import os
from pymongo import MongoClient
from datetime import datetime
from config import Config

# DBHandler क्लास अब __init__ में Mongo Client को कॉल नहीं करेगी
class DBHandler:
    def __init__(self):
        # कनेक्शन को खाली रखें
        self.client = None
        self.db = None
        self.users = None

    def connect(self):
        """Initializes the MongoDB connection using Config.MONGO_URI."""
        if not self.client:
            # केवल तभी कनेक्ट करें जब main.py इसे कॉल करे
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client["MovieBotDB"]
            self.users = self.db["users"]
    
    # बाकी सारे functions (add_new_user, set_admin, is_admin) ज्यों के त्यों रहेंगे, 
    # पर यह सुनिश्चित करें कि वे self.users का उपयोग करने से पहले self.client मौजूद हो।

# db = DBHandler() <--- इस लाइन को हटाएं!
