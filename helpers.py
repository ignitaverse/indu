from datetime import datetime

def format_dt(dt: datetime) -> str:
    return dt.strftime("%d-%m-%Y %H:%M:%S")

def is_private(chat) -> bool:
    return chat.type == "private"
