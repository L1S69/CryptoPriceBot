import telebot  # Library for creating Telegram bot


def create_keyboard(cols: int, buttons: list[str]):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=cols,
                                                 resize_keyboard=True)
    # Create a new instance of ReplyKeyboardMarkup with given number of columns and ability to resize

    keyboard.add(*buttons)  # Add each button in the list to the keyboard
    return keyboard  # Return the created keyboard
