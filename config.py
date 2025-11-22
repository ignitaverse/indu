from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    MONGO_URI = os.getenv("MONGO_URI")
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
    LOG_CHAT_ID = int(os.getenv("LOG_CHAT_ID", "0"))

    @staticmethod
    def validate():
        assert Config.BOT_TOKEN, "BOT_TOKEN must be set in .env file"
        assert Config.MONGO_URI, "MONGO_URI must be set in .env file"
