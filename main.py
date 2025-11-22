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
# ✅ FIX 5: DBHandler class को import करें
from database.db_handler import DBHandler 

# ✅ FIX 6: global DB instance को घोषित करें
db = None 

# ... (logging setup and ping function) ...

def main() -> None:
    global db # ग्लोबल वेरिएबल को मॉडिफाई करने के लिए 'global' कीवर्ड का उपयोग करें
    
    Config.validate()
    
    # -----------------------------------------------
    # 🛑 FIX 7: DB connection को Config validation के बाद शुरू करें
    # -----------------------------------------------
    try:
        db = DBHandler() # DBHandler का इंस्टेंस बनाएं
        db.connect() # अब connect() कॉल करें
        logger.info("MongoDB connected successfully.")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        return # अगर DB कनेक्ट न हो तो बॉट को रोक दें
    # -----------------------------------------------

    application = Application.builder().token(Config.BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("promoteme", promote_me))

    logger.info("Bot polling started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
