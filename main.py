# main (4).py (Updated Code Snippet)
from handlers.start_handler import start_command
from handlers.admin_handler import promote_me
from database.db_handler import db # db_handler से db instance import करें

# ... (logging setup) ...

def main() -> None:
    Config.validate()
    
    # NEW STEP: Config validation के बाद DB connection शुरू करें
    try:
        db.connect()
        logger.info("MongoDB connected successfully.")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        return # अगर DB कनेक्ट न हो तो बॉट को रोक दें

    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # ... (rest of the handlers) ...
