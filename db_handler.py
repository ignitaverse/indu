# MongoDB से संबंधित हैंडलिंग यहाँ करें (उदाहरण के लिए, कनेक्शन बनाना)
from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_URI)
db = client['your_database_name']

def get_user_collection():
    return db['users']
