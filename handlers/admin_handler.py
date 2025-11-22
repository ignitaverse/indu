from telegram import Update
from telegram.ext import ContextTypes
from config import Config
# ❌ OLD: from database.db_handler import DBHandler (यह यहाँ आवश्यक नहीं है)
from database.db_handler import DBHandler 

# --------------------------------------------------------------------------
# ✅ FIX 1: db instance को main.py से इम्पोर्ट करें
# यह एक सामान्य हैक है, जो NameError को ठीक करता है।
try:
    from main import db as global_db
except ImportError:
    # अगर local testing में ImportError आए, तो dummy object बना लें।
    global_db = DBHandler()
# --------------------------------------------------------------------------

def is_owner(user_id: int) -> bool:
    return user_id == Config.ADMIN_ID

# ... (बाकी is_admin फ़ंक्शन) ...

async def promote_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not is_owner(user.id):
        await update.message.reply_text("❌ Ye command sirf owner ke liye hai.")
        return
    
    # ✅ FIX 2: global_db का उपयोग करें
    if global_db and global_db.client: # सुनिश्चित करें कि कनेक्शन खुला है
        global_db.set_admin(user.id, True)
        await update.message.reply_text("✅ Tumhe MovieBot admin bana diya gaya hai.")
    else:
        await update.message.reply_text("❌ Database abhi tak connect nahi hua hai ya koi galti hai.")

# ... (बाकी फ़ंक्शन) ...
