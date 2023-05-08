import requests
from pycoingecko import CoinGeckoAPI
import telebot

token = "**********************************************"
qr_gen_bot = telebot.TeleBot(token)

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

cg = CoinGeckoAPI()

def get_crypto_price(coin):
    id = cg.search(coin)["coins"][0]["id"]
    crypto_data = cg.get_price(ids=id, vs_currencies='usd')
    price = crypto_data[id]['usd']
    return [id, price]


@qr_gen_bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    qr_gen_bot.send_message(message.chat.id,
                            f"Hello, {message.from_user.first_name}, what cryptocurrency price are you interested in?",
                            reply_markup=keyboard)

@qr_gen_bot.message_handler(content_types=["text"])
def get_text_messages(message):
    text = message.text
    data = get_crypto_price(text)
    coin = data[0]
    price = data[1]
    qr_gen_bot.send_message(message.chat.id, f"The price of {coin} is ${price:.2f}", reply_markup=keyboard)


qr_gen_bot.infinity_polling()
