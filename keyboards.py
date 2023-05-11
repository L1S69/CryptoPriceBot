import telebot # Library for creating Telegram bot 
from typing import List

def create_keyboard(cols: int, buttons: List[str]):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=cols, resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard