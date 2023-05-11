import telebot # Library for creating Telegram bot

import config
import dbmanager
import cgapimanager
import keyboards


bot = telebot.TeleBot(config.token)

# Create custom keyboard with cryptocurrency buttons
cryptos = keyboards.create_keyboard(3, config.cryptos)

# Create custom keyboards for Settings
settings = keyboards.create_keyboard(1, config.settings)
currencies = keyboards.create_keyboard(2, config.supported_fiat_currencies)
languages = keyboards.create_keyboard(2, list(config.supported_languages.keys()))

# Handler for /start and /help commands
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    # Send welcome message with custom keyboard
    bot.send_message(message.chat.id,
                            f"Hello, {message.from_user.first_name}, what cryptocurrency price are you interested in?",
                            reply_markup=keyboard)

# Handler for /settings command
@bot.message_handler(commands=["settings"])
def send_settings(message):
    bot.send_message(message.chat.id, "What settings do you want change?", reply_markup=settings)
    bot.register_next_step_handler(message, select_setting)

def select_setting(message):
    if message.text == 'Select language':
        bot.send_message(message.chat.id, "Choose language", reply_markup=languages)
        bot.register_next_step_handler(message, set_language)
    elif message.text == 'Select currency':
        bot.send_message(message.chat.id, "What fiat currency do you want to view the prices in?", reply_markup=currencies)
        bot.register_next_step_handler(message, set_fiat_currency)
    else:
        bot.send_message(message.chat.id, "An error has occurred?", reply_markup=cryptos)

def set_fiat_currency(message):
    if message.text in config.supported_fiat_currencies:
        fiat_currency = message.text
        dbmanager.set_data(message.chat.id, "currency", fiat_currency)
        # Notify user that his default fiat currency was changed
        bot.send_message(message.chat.id, f"You've successfully set {fiat_currency} as default fiat currency", reply_markup=cryptos)
    else:
        # Notify user that his default fiat currency was NOT changed
        bot.send_message(message.chat.id, f"Can't set {message.text} as default fiat currency", reply_markup=cryptos)

def set_language(message):
    if config.supported_languages[message.text]:
        dbmanager.set_data(message.chat.id, "language", config.supported_languages[message.text])
        # Notify user that his default fiat currency was changed
        bot.send_message(message.chat.id, f"You've successfully set {message.text} as default fiat currency", reply_markup=cryptos)

# Handler for text messages received from users
@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    text = message.text # Get the text message from the user
    currency = dbmanager.get_data(message.chat.id, "currency", "usd") # Get user's default fiat currency
    language = dbmanager.get_data(message.chat.id, "language", "en")
    print(language)
    data = cgapimanager.get_crypto_price(text, currency) # Call get_crypto_price function to get the cryptocurrency data
    
    # Extract cryptocurrency ID and USD price from the data
    coin = data[0]
    price = data[1]
    
    # Send the cryptocurrency price to the user
    bot.send_message(message.chat.id, f"The price of {coin} is {price:.2f} {currency}", reply_markup=cryptos)

# Start the bot
bot.infinity_polling()
