from pyrogram import filters
from pyrogram.types import Message

async def start_command(client, message: Message):
    await message.reply("Hello! This is the start command!")
