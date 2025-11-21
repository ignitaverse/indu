from telegram import Update
from telegram.ext import ContextTypes
from config import Config
# ❌ OLD: from database.db_handler import DBHandler
# ✅ NEW: .db_handler को इम्पोर्ट करें (यह मानकर कि admin_handler, database के बराबर फ़ोल्डर में है)
from ..database.db_handler import DBHandler  # यह सुनिश्चित करें कि यह काम करता है

# अगर ऊपर वाला काम नहीं करता है, तो इसे आज़माएं:
# from database.db_handler import DBHandler

# सुनिश्चित करें कि DBHandler का इनिशियलाइज़ेशन main.py में connection के बाद हो (पिछले सुझाव के अनुसार)
# फिलहाल, आप इसे (DBHandler()) हटाकर main.py में एक ग्लोबल variable बना सकते हैं

db = DBHandler() # इसे main.py में इनिशियलाइज़ करने के बाद उपयोग करें
# ...
