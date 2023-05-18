import telebot # Library for creating Telegram bot

import config
import dbmanager
import cgapimanager
import tlmanager
import keyboards

bot = telebot.TeleBot(config.token)

# Create custom keyboard with cryptocurrency buttons
cryptos = keyboards.create_keyboard(3, config.cryptos)

# Create custom keyboards for Settings
currencies = keyboards.create_keyboard(2, config.supported_fiat_currencies)
languages = keyboards.create_keyboard(2, list(config.supported_languages.keys()))

# Handler for /start and /help commands
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    lang = tlmanager.get_language(message.chat.id)
    # Send welcome message with custom keyboard
    bot.send_message(message.chat.id,
                            f"{lang[0][0]}{message.from_user.first_name}{lang[0][1]}",
                            reply_markup=cryptos)

# Handler for /settings command
@bot.message_handler(commands=["settings"])
def send_settings(message):
    lang = tlmanager.get_language(message.chat.id)
    bot.send_message(message.chat.id, lang[1], reply_markup=keyboards.create_keyboard(2, [lang[2], lang[4]]))
    bot.register_next_step_handler(message, select_setting)

def select_setting(message):
    lang = tlmanager.get_language(message.chat.id)
    if message.text == lang[2]:
        bot.send_message(message.chat.id, lang[3], reply_markup=languages)
        bot.register_next_step_handler(message, set_language)
    elif message.text == lang[4]:
        bot.send_message(message.chat.id, lang[5], reply_markup=currencies)
        bot.register_next_step_handler(message, set_fiat_currency)
    else:
        bot.send_message(message.chat.id, lang[6], reply_markup=cryptos)

def set_fiat_currency(message):
    lang = tlmanager.get_language(message.chat.id)
    if message.text in config.supported_fiat_currencies:
        fiat_currency = message.text
        dbmanager.set_data(message.chat.id, "currency", fiat_currency)
        # Notify user that his default fiat currency was changed
        bot.send_message(message.chat.id, f"{lang[9][0]}{fiat_currency}{lang[9][1]}", reply_markup=cryptos)
    else:
        # Notify user that his default fiat currency was NOT changed
        bot.send_message(message.chat.id, lang[6], reply_markup=cryptos)

def set_language(message):
    if config.supported_languages[message.text]:
        dbmanager.set_data(message.chat.id, "language", config.supported_languages[message.text])
        # Notify user that his default fiat currency was changed
        bot.send_message(message.chat.id, tlmanager.languages[config.supported_languages[message.text]][7], reply_markup=cryptos)

# Handler for text messages received from users
@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    text = message.text # Get the text message from the user
    currency = dbmanager.get_data(message.chat.id, "currency", "usd") # Get user's default fiat currency
    lang = tlmanager.get_language(message.chat.id)
    data = cgapimanager.get_crypto_price(text, currency) # Call get_crypto_price function to get the cryptocurrency data
    
    print(data)
    # Extract cryptocurrency ID and USD price from the data
    coin = data[0]
    price = data[1]
    
    # Send the cryptocurrency price to the user
    reply = (f"{lang[8][0]}{coin}{lang[8][1]}{price:.2f} {currency}{lang[8][2]}\n"
             f"{lang[10][0]}{data[2]} {currency}{lang[10][1]}\n"
             f"{lang[11]}{data[3]} {currency}\n"
             f"{lang[12][0]}{data[4]}%{lang[12][1]}")
    bot.send_message(message.chat.id, reply, reply_markup=cryptos)

# Start the bot
bot.infinity_polling()
