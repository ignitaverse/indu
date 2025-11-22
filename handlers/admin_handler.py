from pyrogram import filters
from pyrogram.types import Message
import config

import config

async def admin_command(client, message):
    if message.from_user.id == config.ADMIN_ID:
        await message.reply("You are admin!")
        else:
        await message.reply("You are not authorized to use this command.")
