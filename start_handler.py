from telegram import Update
from telegram.ext import ContextTypes
# ... (अन्य imports) ...
from database.db_handler import DBHandler 

# ❌ OLD: db = DBHandler()
# ✅ NEW: इसे हटा दें, क्योंकि यह main.py में बनेगा और global scope में सेट होगा।
# ... (बाकी सारा कोड global db variable का उपयोग करेगा, जिसे आपको main.py से पास करना होगा, 
# या temporarilly, हर handler के अंदर db = DBHandler() को call करें जब तक आपको सही तरीका न मिल जाए।)
