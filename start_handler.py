from telegram import Update
from telegram.ext import ContextTypes
from database.db_handler import DBHandler
from config import Config

db = DBHandler()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat

    is_new = db.add_new_user(user.id, user.username, user.first_name)

    if is_new:
        text = (
            f"🌟 Hello <b>{user.first_name}</b>, Welcome to <b>MRKPREMIUM</b>!\n\n"
            "Yahaan tumhe latest Movies, Webseries, Dramas & Films ke download links milenge."
        )
    else:
        text = f"👋 Welcome back, <b>{user.first_name}</b>!"

    await update.message.reply_html(text)

    if is_new and Config.ADMIN_ID:
        await context.bot.send_message(
            chat_id=Config.ADMIN_ID,
            text=f"🚨 New User: {user.first_name} (@{user.username}) joined in {chat.id}",
        )
