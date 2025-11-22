from pyrogram import filters
from pyrogram.types import Message

async def start_command(client, message):
    await message.reply("Hello, welcome!")
