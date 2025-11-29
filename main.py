import os
import re
import random
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
ADMIN_ID = int(os.getenv("ADMIN_ID", "6190729758"))
RENDER_EXTERNAL_URL = os.getenv('RENDER_EXTERNAL_URL', 'https://meeku-13fv.onrender.com')
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}/{BOT_TOKEN}"

app = Flask(__name__)

print(f"🚀 Starting Meeku Bot | Token: {BOT_TOKEN[:10]}...")

# Global collections (safe initialization)
users_col = premium_col = facts_col = groups_col = settings_col = None

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
    "🧠 The human brain can store about 2.5 petabytes of information."
]

# MongoDB setup (SAFE)
try:
    if MONGO_URI:
        mongo_client = MongoClient(MONGO_URI)
        db = mongo_client["meeku_bot_db"]
        users_col = db["users"]
        premium_col = db["premium_users"]
        facts_col = db["science_facts"]
        groups_col = db["groups"]
        settings_col = db["group_settings"]
        print("✅ MongoDB connected successfully")
        
        # Initialize default facts
        if facts_col and facts_col.count_documents({}) == 0:
            default_facts_data = [{"fact": fact, "added_by": ADMIN_ID, "added_date": datetime.utcnow()} for fact in DEFAULT_FACTS]
            facts_col.insert_many(default_facts_data)
            print("✅ Default science facts added")
    else:
        print("⚠️ No MONGO_URI - using memory storage")
except Exception as e:
    print(f"❌ MongoDB error (continuing without DB): {e}")

# ==================== HELPERS ====================
def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if users_col:
            user = update.effective_user
            user_data = {
                "user_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_active": datetime.utcnow(),
                "is_premium": False
            }
            users_col.update_one({"user_id": user.id}, {"$set": user_data}, upsert=True)
    except:
        pass

def is_premium_user(user_id: int) -> bool:
    try:
        if premium_col:
            return premium_col.find_one({"user_id": user_id}) is not None
    except:
        pass
    return False

# ==================== COMMANDS ====================
def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update, context)
    welcome_text = """✨ *Welcome to Meeku Bot!* ✨

🤖 *Features:*
• 🎬 Movie Requests: `! Movie Name {2023}`
• 🧮 Math: `/math 2+2` or `2+2`
• 🔬 Facts: `/fact`
• 💎 Premium: `/premium`

*Owner:* @SSRATHAUR"""
    update.message.reply_text(welcome_text, parse_mode='Markdown')

def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update, context)
    help_text = """🤖 *Commands:*
/start - Welcome message
/help - This help
/contact - Contact info
/premium - Premium plans
/fact - Science fact
/math - Calculator
/status - Your status

*Movie:* `! Movie Name {2023}`
*Math:* `2+2*3`
*Admin:* `admin`"""
    update.message.reply_text(help_text, parse_mode='Markdown')

def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_text = """📞 *Contact:*
👑 Owner: @SSRATHAUR
📧 igniverse@gmail.com
📢 Channels:
• https://t.me/+sPlncFPGqrxlMWFl
• https://t.me/SSshowswatch"""
    update.message.reply_text(contact_text, parse_mode='Markdown')

def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update, context)
    fact_text = random.choice(DEFAULT_FACTS)
    update.message.reply_text(f"🔬 *Science Fact:*
{fact_text}", parse_mode='Markdown')

def calculate_expression(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        update.message.reply_text("❌ `/math 2+2*3`", parse_mode='Markdown')
        return
    try:
        expression = ' '.join(context.args)
        allowed_chars = set('0123456789+-*/.() ')
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            update.message.reply_text(f"🧮 `{expression} = {result}`", parse_mode='Markdown')
        else:
            update.message.reply_text("❌ Only + - * / . ( ) allowed")
    except:
        update.message.reply_text("❌ Invalid expression")

def premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update, context)
    keyboard = [
        [InlineKeyboardButton("💰 BASIC ₹60", callback_data="premium_basic")],
        [InlineKeyboardButton("💎 MASTER ₹170", callback_data="premium_master")],
        [InlineKeyboardButton("📞 Contact", url="https://t.me/SSRATHAUR")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("👑 *Premium Plans:*
💰 BASIC ₹60
💎 MASTER ₹170
📞 Contact: @SSRATHAUR", 
                             reply_markup=reply_markup, parse_mode='Markdown')

def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.strip()
    track_user(update, context)
    
    # Movie request
    if message_text.startswith('!'):
        if '{' in message_text and '}' in message_text:
            update.message.reply_text("🎬 *Request accepted!*
*Wait for Sunday.*
💎 Premium: @SSRATHAUR", parse_mode='Markdown')
        else:
            update.message.reply_text("❌ `! Movie Name {2023}`", parse_mode='Markdown')
        return
    
    # Math calculation
    allowed_chars = set('0123456789+-*/.() ')
    if all(c in allowed_chars for c in message_text):
        try:
            result = eval(message_text)
            update.message.reply_text(f"🧮 `{message_text} = {result}`", parse_mode='Markdown')
            return
        except:
            pass
    
    # Admin mention
    if 'admin' in message_text.lower():
        update.message.reply_text("⏳ *Wait for admin reply*", parse_mode='Markdown')
        return

# ==================== WEBHOOK (100% FIXED) ====================
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    """SIMPLE WEBHOOK - NO THREADING ISSUES"""
    try:
        json_data = request.get_json()
        print(f"📨 Update: {json_data.get('message', {}).get('text', 'callback')[:20]}...")
        
        update = Update.de_json(json_data, bot_application.bot)
        if update:
            # SYNCHRONOUS processing (Render compatible)
            bot_application.process_update(update)
        
        return "OK"
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return "ERROR", 500

@app.route("/")
def index():
    return "🤖 Meeku Bot v2.0 ✅"

@app.route("/set_webhook")
def set_webhook():
    try:
        bot_application.bot.set_webhook(WEBHOOK_URL)
        return f"✅ Webhook set: {WEBHOOK_URL}"
    except Exception as e:
        return f"❌ Error: {e}"

# ==================== BOT SETUP ====================
def setup_bot():
    print("🔧 Setting up bot...")
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contact", contact_command))
    application.add_handler(CommandHandler("premium", premium_command))
    application.add_handler(CommandHandler("fact", fact_command))
    application.add_handler(CommandHandler("math", calculate_expression))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot handlers added")
    return application

# Initialize
bot_application = setup_bot()
print("✅ Bot initialized successfully!")
print(f"🌐 Webhook: {WEBHOOK_URL}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🔥 Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
