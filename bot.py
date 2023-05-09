# Import required libraries
import requests # for making HTTP requests
from pycoingecko import CoinGeckoAPI # for fetching crypto price data
import telebot # for creating Telegram bot

# Telegram bot token obtained from BotFather
token = "**********************************************"
# Initialize the bot with the token
bot = telebot.TeleBot(token)

keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3)

# Create custom keyboard with cryptocurrency buttons
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

# Initialize CoinGeckoAPI object
cg = CoinGeckoAPI()

# Function to fetch the cryptocurrency price
def get_crypto_price(coin):
    id = cg.search(coin)["coins"][0]["id"] # Search the coin on CoinGecko API and get its ID
    
    crypto_data = cg.get_price(ids=id, vs_currencies='usd') # Fetch the price data for the specified cryptocurrency
    price = crypto_data[id]['usd'] # Get the USD price for the specified cryptocurrency
    
    return [id, price] # Return the cryptocurrency ID and USD price in a list

# Handler for /start and /help commands
@qr_gen_bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    # Send welcome message with custom keyboard
    bot.send_message(message.chat.id,
                            f"Hello, {message.from_user.first_name}, what cryptocurrency price are you interested in?",
                            reply_markup=keyboard)

# Handler for text messages received from users
@qr_gen_bot.message_handler(content_types=["text"])
def get_text_messages(message):
    text = message.text # Get the text message from the user
    data = get_crypto_price(text) # Call get_crypto_price function to get the cryptocurrency data
    
    # Extract cryptocurrency ID and USD price from the data
    coin = data[0]
    price = data[1]
    
    # Send the cryptocurrency price to the user
    bot.send_message(message.chat.id, f"The price of {coin} is ${price:.2f}", reply_markup=keyboard)

# Start the bot
bot.infinity_polling()
