# ... (imports) ...
from config import Config
from handlers.start_handler import start_command
from handlers.admin_handler import promote_me
from database.db_handler import DBHandler # DBHandler class को import करें

# Global DB instance variable
global_db_instance = None 

# ... (ping function) ...

def main() -> None:
    global global_db_instance # ग्लोबल वेरिएबल को मॉडिफाई करने के लिए
    
    Config.validate()
    
    # -----------------------------------------------
    # 🛑 FIX: DB connection को Config validation के बाद शुरू करें
    # -----------------------------------------------
    try:
        # DBHandler का इंस्टेंस बनाएं
        global_db_instance = DBHandler()
        # फिर connection शुरू करें
        global_db_instance.connect()
        logger.info("MongoDB connected successfully.")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        # अगर DB कनेक्ट न हो तो बॉट को रोक दें
        return 

    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # ... (handlers) ...
    
    logger.info("Bot polling started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
