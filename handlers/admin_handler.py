from telegram import Update
from telegram.ext import ContextTypes
from config import Config
# ✅ FIX 1: अब हम db_handler से DBHandler क्लास नहीं, बल्कि get_db_instance फ़ंक्शन इम्पोर्ट करेंगे।
from database.db_handler import get_db_instance
# is_private function को helpers से import करते हैं
from helpers import is_private 


# -- Owner Check --
def is_owner(user_id: int) -> bool:
    """Checks if the user ID is the configured owner ID."""
    return user_id == Config.ADMIN_ID

# -- Admin Check --
def is_admin(user_id: int) -> bool:
    """Checks if the user ID is marked as an admin in the database or is the owner."""
    # ✅ FIX 2: DB access के लिए get_db_instance() का उपयोग करें
    db = get_db_instance()
    return is_owner(user_id) or db.is_admin(user_id)


# -- PROMOTE ME COMMAND --
async def promote_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    # ✅ FIX 3: DB instance को केवल तभी प्राप्त करें जब जरूरत हो
    db = get_db_instance()
    
    if not is_owner(user.id):
        await update.message.reply_text("❌ Ye command sirf owner ke liye hai.")
        return
        
    db.set_admin(user.id, True)
    await update.message.reply_text("✅ Tumhe MovieBot admin bana diya gaya hai.")


# -- STATS COMMAND --
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows bot statistics (total users, etc.)."""
    user = update.effective_user
    
    # ✅ FIX 4: DB instance को केवल तभी प्राप्त करें जब जरूरत हो
    db = get_db_instance()
    
    # Check for Admin/Owner permission
    if not is_admin(user.id):
        await update.message.reply_text("❌ Aapke paas is command ko use karne ki anumati nahi hai.")
        return

    # Get stats from DB
    total_users = db.users.count_documents({})
    
    stats_message = (
        f"📊 **BOT STATISTICS** 📊\n\n"
        f"👥 **Total Users:** {total_users}\n"
        f"📢 **Log Chat ID:** <code>{Config.LOG_CHAT_ID}</code>"
    )
    
    await update.message.reply_html(stats_message)


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
        # Broadcasting the replied message (Media/Text)
        message_to_send = update.message.reply_to_message
        await update.message.reply_text("⏳ Broadcast shuru ho raha hai... (It may take a while for large user bases)")
        
        # We need a separate function to handle media/text broadcast by reply
        # For simplicity, we only handle text for now unless media logic is implemented
        if message_to_send.text:
            await send_text_broadcast(context, message_to_send.text)
        else:
             await update.message.reply_text("❌ Media broadcast logic abhi implemented nahi hai. Kripya sirf text ya reply ka upyog karein.")
        
    else:
        # Broadcasting the text following /broadcast
        text = update.message.text.split(" ", 1)[1]
        await update.message.reply_text("⏳ Broadcast shuru ho raha hai... (It may take a while for large user bases)")
        await send_text_broadcast(context, text)


# Helper function to send simple text broadcast (for non-reply broadcasts)
async def send_text_broadcast(context: ContextTypes.DEFAULT_TYPE, text: str):
    """Sends a text message to all users using the globally accessible DB."""
    
    # ✅ FIX 5: DB instance को यहां प्राप्त करें
    db = get_db_instance()
    
    users = db.users.find({}, {"_id": 1}) # Fetch only the user IDs
    success_count = 0
    fail_count = 0
    
    for user_doc in users:
        user_id = user_doc["_id"]
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=text,
                parse_mode='HTML'
            )
            success_count += 1
        except Exception:
            # Common exceptions: Bot was blocked by the user or chat not found
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
