from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from database.db_handler import get_db_instance 
# ❌ OLD: from helpers import is_private 

# ✅ FIX: is_private function को helpers से import करें (जैसा कि पहले ही प्लान किया गया था)
from helpers import is_private 

import logging

logger = logging.getLogger(__name__)

# -- Owner Check --
def is_owner(user_id: int) -> bool:
    """Checks if the user ID is the configured owner ID."""
    return user_id == Config.ADMIN_ID

# -- Admin Check --
def is_admin(user_id: int) -> bool:
    """Checks if the user ID is marked as an admin in the database or is the owner."""
    # ✅ FIX 2: DB access के लिए get_db_instance() का उपयोग करें
    try:
        db = get_db_instance()
        return is_owner(user_id) or db.is_admin(user_id)
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return is_owner(user_id) # Fallback to owner check if DB fails


# -- PROMOTE ME COMMAND --
async def promote_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    if not is_owner(user.id):
        await update.message.reply_text("❌ Ye command sirf owner ke liye hai.")
        return
    
    # ✅ FIX 3: DB instance को केवल तभी प्राप्त करें जब जरूरत हो
    try:
        db = get_db_instance()
        db.set_admin(user.id, True)
        await update.message.reply_text("✅ Tumhe MovieBot admin bana diya gaya hai.")
    except Exception as e:
        await update.message.reply_text(f"❌ Database error: {e}")
        logger.error(f"Error in promote_me: {e}")


# -- STATS COMMAND --
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows bot statistics (total users, etc.)."""
    user = update.effective_user
    
    # Check for Admin/Owner permission
    if not is_admin(user.id):
        await update.message.reply_text("❌ Aapke paas is command ko use karne ki anumati nahi hai.")
        return

    # ✅ FIX 4: DB instance को केवल तभी प्राप्त करें जब जरूरत हो
    try:
        db = get_db_instance()
        # Get stats from DB
        total_users = db.users.count_documents({})
        
        stats_message = (
            f"📊 **BOT STATISTICS** 📊\n\n"
            f"👥 **Total Users:** {total_users}\n"
            f"📢 **Log Chat ID:** <code>{Config.LOG_CHAT_ID}</code>"
        )
        
        await update.message.reply_html(stats_message)
    except Exception as e:
        await update.message.reply_text(f"❌ Database error while fetching stats: {e}")
        logger.error(f"Error in stats_command: {e}")


# -- BROADCAST COMMAND --
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcasts a message to all users in the database."""
    user = update.effective_user
    
    # Check for Admin/Owner permission
    if not is_admin(user.id):
        await update.message.reply_text("❌ Aapke paas is command ko use karne ki anumati nahi hai.")
        return

    # 1. Check if the command has a message attached
    if not context.args and not update.message.reply_to_message:
        await update.message.reply_text(
            "📢 **Usage:** /broadcast <message> OR /broadcast while replying to a message.\n"
            "⚠️ Note: HTML formatting is supported."
        )
        return

    # 2. Get the content to broadcast
    if update.message.reply_to_message:
        message_to_send = update.message.reply_to_message
        await update.message.reply_text("⏳ Broadcast shuru ho raha hai... (It may take a while for large user bases)")
        
        # Simple text handling for replied message
        if message_to_send.text:
            await send_text_broadcast(context, message_to_send.text)
        else:
             await update.message.reply_text("❌ Media broadcast logic abhi implemented nahi hai. Kripya sirf text ya reply ka upyog karein.")
        
    else:
        text = update.message.text.split(" ", 1)[1]
        await update.message.reply_text("⏳ Broadcast shuru ho raha hai... (It may take a while for large user bases)")
        await send_text_broadcast(context, text)


# Helper function to send simple text broadcast (for non-reply broadcasts)
async def send_text_broadcast(context: ContextTypes.DEFAULT_TYPE, text: str):
    """Sends a text message to all users using the globally accessible DB."""
    
    try:
        # ✅ FIX 5: DB instance को यहां प्राप्त करें
        db = get_db_instance()
        
        users = db.users.find({}, {"_id": 1}) # Fetch only the user IDs
        success_count = 0
        fail_count = 0
        
        # Context.bot का उपयोग करें, क्योंकि यह handler फ़ंक्शन नहीं है
        bot_instance = context.bot
        
        for user_doc in users:
            user_id = user_doc["_id"]
            try:
                await bot_instance.send_message(
                    chat_id=user_id,
                    text=text,
                    parse_mode='HTML'
                )
                success_count += 1
            except Exception as e:
                # Common exceptions: Bot was blocked by the user or chat not found
                logger.error(f"Broadcast failed for user {user_id}: {e}")
                fail_count += 1
                
        # Send summary to the admin who initiated the broadcast
        summary = (
            f"✅ **Broadcast Completed!**\n"
            f"   Sent to: {success_count} users\n"
            f"   Failed: {fail_count} users (Blocked/Deleted)"
        )
        await context.bot.send_message(
            chat_id=Config.ADMIN_ID, 
            text=summary,
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error(f"Critical error during broadcast: {e}")
        await context.bot.send_message(
            chat_id=Config.ADMIN_ID, 
            text=f"❌ **CRITICAL ERROR** during broadcast: {e}",
            parse_mode='HTML'
        )
