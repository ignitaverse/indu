from pyrogram import filters
from pyrogram.types import Message
import config

async def admin_command(client, message: Message):
    if message.from_user.id == config.ADMIN_ID:
        await message.reply("Admin command executed.")
    else:
        await message.reply("You are not authorized to use this command.")
