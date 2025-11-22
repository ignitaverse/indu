from telegram import Update
from telegram.ext import ContextTypes
from config import Config
# ❌ OLD: from database.db_handler import DBHandler (इसे main.py में ही छोड़ दें)
# -----------------------------------------------------------------------
# ✅ FIX 3: main.py से ग्लोबल DB instance को इम्पोर्ट करने की कोशिश करें।
try:
    from main import db as global_db
except ImportError:
    # यह Render पर काम करेगा, local testing में error दे सकता है।
    # हम DB access को 'global_db' के माध्यम से करेंगे।
    global_db = None 
# -----------------------------------------------------------------------


def is_owner(user_id: int) -> bool:
    return user_id == Config.ADMIN_ID

# ... (बाकी is_admin फ़ंक्शन) ...

async def promote_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not is_owner(user.id):
        await update.message.reply_text("❌ Ye command sirf owner ke liye hai.")
        return
    
    # ✅ FIX 4: global_db का उपयोग करें
    if global_db:
        global_db.set_admin(user.id, True)
        await update.message.reply_text("✅ Tumhe MovieBot admin bana diya gaya hai.")
    else:
        await update.message.reply_text("❌ Database abhi tak connect nahi hua hai.")
