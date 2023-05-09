# Import required libraries
import requests # for making HTTP requests
from pycoingecko import CoinGeckoAPI # for fetching crypto price data
import telebot # for creating Telegram bot
import sqlite3


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

# Create custom keyboard for Settings
settings = telebot.types.ReplyKeyboardMarkup(row_width=3)

button_usd = telebot.types.KeyboardButton('USD')
button_eur = telebot.types.KeyboardButton('EUR')
button_rub = telebot.types.KeyboardButton('RUB')
button_gpb = telebot.types.KeyboardButton('GPB')
button_uah = telebot.types.KeyboardButton('UAH')
button_kzt = telebot.types.KeyboardButton('KZT')
button_byn = telebot.types.KeyboardButton('BYN')
button_idr = telebot.types.KeyboardButton('IDR')
button_ils = telebot.types.KeyboardButton('ILS')
settings.add(button_usd, button_eur, button_rub,
             button_gpb, button_uah, button_kzt,
             button_byn, button_idr, button_ils)

# Initialize CoinGeckoAPI object
cg = CoinGeckoAPI()

# Fiat currencies that are supported
supported_fiat_currencies = ['USD', 'EUR', 'RUB', 'GPB', 'UAH', 'KZT', 'BYN', 'IDR', 'ILS']

def get_fiat_currency(chat_id):
    conn = sqlite3.connect('preferences.db') # Connect to the database
    cursor = conn.cursor() # Create a cursor object to execute SQL queries
    cursor.execute("SELECT currency FROM user_preferences WHERE chat_id = ?", (chat_id,)) # Get prefered fiat currency of user by his chat id
    result = cursor.fetchone() # Get the first row of the result
    currency = result[0] if result else "usd" # Get the currency if the result is not empty, otherwise set it to USD
    return currency

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
def get_text_messages(message):
    bot.send_message(message.chat.id, "What fiat currency do you want to view the prices in?", reply_markup=settings)
    bot.register_next_step_handler(message, set_fiat_currency)

def set_fiat_currency(message):
    if message.text in supported_fiat_currencies:
        fiat_currency = message.text
        conn = sqlite3.connect('preferences.db') # Connect to the database
        cursor = conn.cursor() # Create a cursor object to execute SQL queries

        # Execute SQL query to insert or update user preferences in the user_preferences table
        # The query replaces the existing row with the new values if the chat_id already exists in the table
        cursor.execute("INSERT OR REPLACE INTO user_preferences (chat_id, currency, language) VALUES (?, ?, ?)", (message.chat.id, fiat_currency, "en"))
        conn.commit() # Commit changes to the database

        # Notify user that his default fiat currency was changed
        bot.send_message(message.chat.id, f"You've successfully set {fiat_currency} as default fiat currency", reply_markup=keyboard)
    else:
        # Notify user that his default fiat currency was NOT changed
        bot.send_message(message.chat.id, f"Can't set {message.text} as default fiat currency", reply_markup=keyboard)

# Handler for text messages received from users
@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    text = message.text # Get the text message from the user
    currency = get_fiat_currency(message.chat.id) # Get user's default fiat currency
    data = get_crypto_price(text, currency) # Call get_crypto_price function to get the cryptocurrency data
    
    # Extract cryptocurrency ID and USD price from the data
    coin = data[0]
    price = data[1]
    
    # Send the cryptocurrency price to the user
    bot.send_message(message.chat.id, f"The price of {coin} is {price:.2f} {currency}", reply_markup=keyboard)

# Start the bot
bot.infinity_polling()
