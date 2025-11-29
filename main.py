import os
import re
import random
import threading
import asyncio
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes, CallbackQueryHandler
)
from pymongo import MongoClient
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_ID = int(os.getenv("ADMIN_ID", 6190729758))
LOG_CHAT_ID = os.getenv("LOG_CHAT_ID", "-1001930405482")

# Webhook URL
RENDER_EXTERNAL_URL = os.getenv('RENDER_EXTERNAL_URL', 'https://meeku-13fv.onrender.com')
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}/{BOT_TOKEN}"
app = Flask(__name__)

# Default science facts
DEFAULT_FACTS = [
    "🔬 The Earth revolves around the Sun at about 67,000 miles per hour.",
    "🌍 Water covers about 71% of the Earth's surface.",
    "💪 The human body has over 600 muscles.",
    "⚡ Light travels at 299,792 kilometers per second in vacuum.",
    "⭐ There are more stars in the universe than grains of sand on all Earth's beaches.",
    "🍯 Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs!",
    "🐙 Octopuses have three hearts and blue blood.",
    "🪐 A day on Venus is longer than a year on Venus.",
    "🍌 Bananas are berries, but strawberries aren't.",
    "🧠 The human brain can store about 2.5 petabytes of information.",
    "⚡ A lightning bolt is five times hotter than the sun's surface.",
    "🌊 The ocean contains enough salt to cover all continents in a layer 500 feet thick.",
    "🐜 Ants never sleep and can lift 50 times their body weight.",
    "🔥 Diamonds can burn at high temperatures in oxygen.",
    "🌡️ The coldest temperature ever recorded on Earth was -128.6°F in Antarctica."
]

# MongoDB setup
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["meeku_bot_db"]
    users_col = db["users"]
    premium_col = db["premium_users"]
    facts_col = db["science_facts"]
    groups_col = db["groups"]
    settings_col = db["group_settings"]
    print("✅ MongoDB connected successfully")
    
    # Initialize default facts if collection is empty
    if facts_col.count_documents({}) == 0:
        default_facts_data = [{"fact": fact, "added_by": ADMIN_ID, "added_date": datetime.utcnow()} for fact in DEFAULT_FACTS]
        facts_col.insert_many(default_facts_data)
        print("✅ Default science facts added to database")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")

# ==================== USER MANAGEMENT SYSTEM ====================
def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Track user data in MongoDB"""
    try:
        if 'users_col' in globals():
            user = update.effective_user
            user_data = {
                "user_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "last_active": datetime.utcnow(),
                "is_premium": False
            }
            users_col.update_one(
                {"user_id": user.id},
                {"$set": user_data},
                upsert=True
            )
    except Exception as e:
        print(f"User tracking error: {e}")

def is_premium_user(user_id: int) -> bool:
    """Check if user has premium access"""
    try:
        if 'premium_col' in globals():
            premium_user = premium_col.find_one({"user_id": user_id})
            return premium_user is not None
    except:
        pass
    return False

# ==================== MOVIE REQUEST SYSTEM ====================
def handle_movie_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle movie requests with pattern [! Movie Name {year}]"""
    message_text = update.message.text.strip()
    
    # Check for movie request pattern
    movie_pattern = r'^!\s*(.+?)\s*\{(\d{4})\}$'
    match = re.match(movie_pattern, message_text, re.IGNORECASE)
    
    if match:
        movie_name = match.group(1).strip()
        movie_year = match.group(2).strip()
        
        # Track user activity
        track_user(update, context)
        
        response = f"""🎬 *Request accepted* ✅

*Name:* {movie_name} ({movie_year}) 🎬

*Wait for Sunday.*

⚠️ *If you want this file now then buy Premium membership.*

✔️ Jisme aapko 15+ channels milenge

*Contact for premium:* @SSRATHAUR"""
        update.message.reply_text(response, parse_mode='Markdown')
        return True
    
    # If pattern not matched but starts with '!', show format error
    elif message_text.startswith('!'):
        response = """❌ *Please follow these rules:*

1. Type correct spelling for request
2. Check this spelling on Google before request
3. Mention release year too

*Correct Format:* `! Movie Name {2023}`

*Example:* `! Avatar {2009}`"""
        update.message.reply_text(response, parse_mode='Markdown')
        return True
    
    return False

# ==================== MATH CALCULATION SYSTEM ====================
def calculate_expression(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate mathematical expressions"""
    if not context.args:
        update.message.reply_text(
            "❌ Please provide a mathematical expression.\n*Example:* `/math 2+2*3`",
            parse_mode='Markdown'
        )
        return
    
    expression = ' '.join(context.args)
    try:
        # Safety check - only allow basic math operations
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            update.message.reply_text("❌ Only basic math operations are allowed: + - * / . ( )")
            return
        
        # Evaluate the expression safely
        result = eval(expression)
        update.message.reply_text(f"🧮 *Calculation Result:*\n`{expression} = {result}`", parse_mode='Markdown')
    except ZeroDivisionError:
        update.message.reply_text("❌ Error: Division by zero is not allowed")
    except Exception as e:
        update.message.reply_text("❌ Error: Invalid mathematical expression")

# ==================== ADMIN MENTION HAND
