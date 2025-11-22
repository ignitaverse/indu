# ... (imports) ...
from database.db_handler import DBHandler
# import main.global_db_instance (यह मुश्किल है)

# ❌ OLD: db = DBHandler()

# ✅ NEW: इस लाइन को हटा दें, और हर DB-required function में DB instance को access करें।
# चूंकि यह जटिल है, हम global_db_instance को main.py से import करने के लिए मजबूर करते हैं (हालांकि यह bad practice है)

# ******************************************************************
# TEMPORARY FIX: main.py से global instance को import करने का प्रयास करें
# ******************************************************************
try:
    from main import global_db_instance as db
except ImportError:
    # अगर main से import नहीं हुआ, तो dummy object बनाएं ताकि Python न क्रैश हो
    print("Warning: Could not import global DB instance from main.py. Creating dummy DBHandler.")
    db = DBHandler()
# ******************************************************************
