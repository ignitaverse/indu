import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    MONGO_URI = os.getenv("MONGO_URI")
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
    LOG_CHAT_ID = int(os.getenv("LOG_CHAT_ID", "0"))  # agar alag log group rakhna ho

    @classmethod
    def validate(cls):
        missing = []
        if not cls.BOT_TOKEN:
            missing.append("BOT_TOKEN")
        if not cls.MONGO_URI:
            missing.append("MONGO_URI")
        if missing:
            raise RuntimeError(f"Missing ENV vars: {', '.join(missing)}")
