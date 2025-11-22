from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from database.db_handler import DBHandler # केवल क्लास को इम्पोर्ट करें

# --------------------------------------------------------------------------
# ✅ FIX 1: global_db को 'db' नाम से main.py से इम्पोर्ट करें
try:
    # main.py में वेरिएबल का नाम 'db' है, इसलिए उसी नाम से इम्पोर्ट करें।
    from main import db 
except ImportError:
    # अगर local testing में ImportError आए, तो dummy object बना लें।
    print("Warning: Could not import global DB instance from main.py. Creating dummy DBHandler.")
    db = DBHandler()
# --------------------------------------------------------------------------

def is_owner(user_id: int) -> bool:
    return user_id == Config.ADMIN_ID

# ... (बाकी is_admin फ़ंक्शन) ...

async def promote_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not is_owner(user.id):
        await update.message.reply_text("❌ Ye command sirf owner ke liye hai.")
        return
    
    # ✅ FIX 2: अब 'global_db' के बजाय सीधे 'db' का उपयोग करें
    if db and db.client: # सुनिश्चित करें कि कनेक्शन खुला है
        db.set_admin(user.id, True)
        await update.message.reply_text("✅ Tumhe MovieBot admin bana diya gaya hai.")
    else:
        await update.message.reply_text("❌ Database abhi tak connect nahi hua hai ya koi galti hai.")

# ... (बाकी फ़ंक्शन) ...
