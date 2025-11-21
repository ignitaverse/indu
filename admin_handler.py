from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from database.db_handler import DBHandler

db = DBHandler()

def is_owner(user_id: int) -> bool:
    return user_id == Config.ADMIN_ID

async def promote_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not is_owner(user.id):
        await update.message.reply_text("❌ Ye command sirf owner ke liye hai.")
        return
    db.set_admin(user.id, True)
    await update.message.reply_text("✅ Tumhe MovieBot admin bana diya gaya hai.")
