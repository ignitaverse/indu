import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from config import Config
from handlers.start_handler import start_command
from handlers.admin_handler import promote_me
# ✅ FIX 1: DBHandler से संबंधित कोई अनावश्यक import नहीं

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🏓 Bot is alive!")

def main() -> None:
    Config.validate()
    
    # ✅ FIX 2: DB connection logic हटा दिया गया है। यह अब get_db_instance() में है।

    application = Application.builder().token(Config.BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("promoteme", promote_me))
    # Note: Stats और Broadcast commands को admin_handler.py में add करें, 
    # यदि आप उन्हें main.py में जोड़ना चाहते हैं तो उनके functions को admin_handler से import करें।

    logger.info("Bot polling started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
