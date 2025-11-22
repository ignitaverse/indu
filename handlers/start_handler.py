from telegram import Update
from telegram.ext import ContextTypes
from config import Config
# database access ke liye
from database.db_handler import get_db_instance 
# ✅ FIX: is_private function ko helpers se import karein
from helpers import is_private
# ✅ FIX 1: get_db_instance को इम्पोर्ट करें
from database.db_handler import get_db_instance 
# ✅ FIX 2: is_private function को helpers से इम्पोर्ट करें
from helpers import is_private 
import logging

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat
    
    # ✅ FIX 3: DB instance को केवल तभी प्राप्त करें जब जरूरत हो
    try:
        db = get_db_instance()
    except Exception as e:
        logger.error(f"Database initialization failed in start_command: {e}")
        await update.message.reply_text("❌ Database connection failed. Please try again later.")
        return

    # Check if user is already in DB and add if new
    new_user = db.add_new_user(user.id, user.username, user.first_name)
    
    # Bot Owner aur Admin ID check
    is_owner_or_admin = (user.id == Config.ADMIN_ID) or db.is_admin(user.id)

    # --- Response Message Construction ---
    if is_private(chat):
        # Private Chat Response
        welcome_message = f"👋 Hello {user.first_name}! Main {context.bot.name} bot hoon.\n\n"
        
        if new_user:
            welcome_message += "🎉 Aapko MovieBot par naya user register kiya gaya hai.\n"
        
        if is_owner_or_admin:
            welcome_message += "\n👑 **Aap Admin hain!** Aap /stats aur /broadcast jaisi commands use kar sakte hain."
        
        await update.message.reply_html(welcome_message)
    else:
        # Group Chat Response
        await update.message.reply_text(
            f"👋 Hello {user.first_name}! Main yahan hu. Kripya mujhe private mein use karein."
        )

# ... (बाकी start_handler functions अगर हों तो) ...
