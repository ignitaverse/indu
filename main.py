import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from config import Config
# ✅ FIX 1: start_command को वापस इम्पोर्ट करें
from handlers.start_handler import start_command 
from handlers.admin_handler import promote_me
# ✅ FIX 2: DBHandler और global db variable से संबंधित कोई अनावश्यक import/declaration नहीं

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🏓 Bot is alive!")

def main() -> None:
    Config.validate()
    
    # DB connection logic हटा दिया गया है। यह अब get_db_instance() में है।

    application = Application.builder().token(Config.BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("promoteme", promote_me))

    logger.info("Bot polling started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
