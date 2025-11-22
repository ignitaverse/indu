from pyrogram import Client, filters
from handlers.start_handler import start_command
from handlers.admin_handler import admin_command
import config

app = Client("my_bot", bot_token=config.BOT_TOKEN)

app.add_handler(filters.command("start")(start_command))
app.add_handler(filters.command("admin")(admin_command))

app.run()
