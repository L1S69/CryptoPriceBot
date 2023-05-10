# Import required libraries
import requests # for making HTTP requests
from pycoingecko import CoinGeckoAPI # for fetching crypto price data
import telebot # for creating Telegram bot
import sqlite3 # for interacting with database


# Telegram bot token obtained from BotFather
token = "**********************************************"
bot = telebot.TeleBot(token)

# Create custom keyboard with cryptocurrency buttons
keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3)

button_btc = telebot.types.KeyboardButton('BTC')
button_eth = telebot.types.KeyboardButton('ETH')
button_ltc = telebot.types.KeyboardButton('LTC')
button_xrp = telebot.types.KeyboardButton('XRP')
button_bch = telebot.types.KeyboardButton('BCH')
button_doge = telebot.types.KeyboardButton('DOGE')
button_ada = telebot.types.KeyboardButton('ADA')
button_dot = telebot.types.KeyboardButton('DOT')
button_link = telebot.types.KeyboardButton('LINK')
keyboard.add(button_btc, button_eth, button_ltc,
             button_xrp, button_bch, button_doge,
             button_ada, button_dot, button_link)

# Create custom keyboards for Settings
settings = telebot.types.ReplyKeyboardMarkup(row_width=1)
button_langs = telebot.types.KeyboardButton('Select language')
button_currs = telebot.types.KeyboardButton('Select currency')
settings.add(button_langs,
             button_currs)

currencies = telebot.types.ReplyKeyboardMarkup(row_width=2)
button_usd = telebot.types.KeyboardButton('USD')
button_eur = telebot.types.KeyboardButton('EUR')
button_rub = telebot.types.KeyboardButton('RUB')
button_gpb = telebot.types.KeyboardButton('GPB')
button_uah = telebot.types.KeyboardButton('UAH')
button_kzt = telebot.types.KeyboardButton('TRY')
button_byn = telebot.types.KeyboardButton('TWD')
button_idr = telebot.types.KeyboardButton('INR')
button_ils = telebot.types.KeyboardButton('ILS')
button_jpy = telebot.types.KeyboardButton('JPY')
currencies.add(button_usd, button_eur,
               button_rub, button_gpb,
               button_uah, button_kzt,
               button_byn, button_idr,
               button_ils, button_jpy)

languages = telebot.types.ReplyKeyboardMarkup(row_width=2)
button_en = telebot.types.KeyboardButton('🇺🇸English')
button_ru = telebot.types.KeyboardButton('🇷🇺Русский')
button_ja = telebot.types.KeyboardButton('🇯🇵日本語')
button_uk = telebot.types.KeyboardButton('🇺🇦Українська')
languages.add(button_en, button_ru,
              button_ja, button_uk)

# Initialize CoinGeckoAPI object
cg = CoinGeckoAPI()

# Fiat currencies that are supported
supported_fiat_currencies = ['USD', 'EUR', 'RUB', 'GPB', 'UAH', 'TRY', 'TWD', 'INR', 'ILS', 'JPY']
supported_languages = {'🇺🇸English': 'en', '🇷🇺Русский': 'ru', '🇯🇵日本語': 'ja', '🇺🇦Українська': 'uk'}

def get_user_data(chat_id, column, default):
    with sqlite3.connect('preferences.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {column} FROM user_preferences WHERE chat_id = ?", (chat_id,)) # Get data by user's chat_id
        result = cursor.fetchone() # Get the first row of the result
        data = result[0] if result else default # Get the value if the result is not empty, otherwise set it to default
        return data

def set_user_data(chat_id, column, value):
    with sqlite3.connect('preferences.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE user_preferences SET {column} = ? WHERE chat_id = ?", (value, chat_id))
        conn.commit()

# Function to fetch the cryptocurrency price
def get_crypto_price(coin, currency):
    id = cg.search(coin)["coins"][0]["id"] # Search the coin on CoinGecko API and get its ID
    
    currency = currency.lower()
    crypto_data = cg.get_price(ids=id, vs_currencies=currency) # Fetch the price data for the specified cryptocurrency
    price = crypto_data[id][currency] # Get default fiat currency price for the specified cryptocurrency
    
    return [id, price] # Return the cryptocurrency ID and default fiat currency price in a list

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
        bot.send_message(message.chat.id, "An error has occurred?", reply_markup=keyboard)

def set_fiat_currency(message):
    if message.text in supported_fiat_currencies:
        fiat_currency = message.text
        set_user_data(message.chat.id, "currency", fiat_currency)
        # Notify user that his default fiat currency was changed
        bot.send_message(message.chat.id, f"You've successfully set {fiat_currency} as default fiat currency", reply_markup=keyboard)
    else:
        # Notify user that his default fiat currency was NOT changed
        bot.send_message(message.chat.id, f"Can't set {message.text} as default fiat currency", reply_markup=keyboard)

def set_language(message):
    if supported_languages[message.text]:
        set_user_data(message.chat.id, "language", supported_languages[message.text])
        # Notify user that his default fiat currency was changed
        bot.send_message(message.chat.id, f"You've successfully set {message.text} as default fiat currency", reply_markup=keyboard)

# Handler for text messages received from users
@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    text = message.text # Get the text message from the user
    currency = get_user_data(message.chat.id, "currency", "usd") # Get user's default fiat currency
    language = get_user_data(message.chat.id, "language", "en")
    print(language)
    data = get_crypto_price(text, currency) # Call get_crypto_price function to get the cryptocurrency data
    
    # Extract cryptocurrency ID and USD price from the data
    coin = data[0]
    price = data[1]
    
    # Send the cryptocurrency price to the user
    bot.send_message(message.chat.id, f"The price of {coin} is {price:.2f} {currency}", reply_markup=keyboard)

# Start the bot
bot.infinity_polling()
