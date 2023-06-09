import telebot  # Library for creating Telegram bot
import os

import config
import dbmanager
import cgapimanager
import thememanager
import tlmanager
import graphmanager
import keyboards

bot = telebot.TeleBot(config.token)

# Create custom keyboard with cryptocurrency buttons
cryptos = keyboards.create_keyboard(3, config.cryptos)

# Create custom keyboards for Settings
currencies = keyboards.create_keyboard(2, config.supported_fiat_currencies)
languages = keyboards.create_keyboard(2, list(config.supported_languages.keys()))
themes = keyboards.create_keyboard(2, list(thememanager.themes.keys()))


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
    bot.send_message(message.chat.id, lang[1], reply_markup=keyboards.create_keyboard(1, [lang[2], lang[4], lang[16]]))
    bot.register_next_step_handler(message, select_setting)


# Handler for /convert command
@bot.message_handler(commands=["convert"])
def send_settings(message):
    lang = tlmanager.get_language(message.chat.id)
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, lang[13], reply_markup=cryptos)
    else:
        args = message.text.split()[1:]
        amount = int(args[0])
        from_curr = args[1]
        to_curr = args[2]
        try:
            conversion_result = cgapimanager.perform_currency_conversion(amount, from_curr, to_curr)
            bot.send_message(message.chat.id,
                             f"{amount}{from_curr.upper()}{lang[14][0]}{conversion_result:.2f}{to_curr.upper()}{lang[14][1]}",
                             reply_markup=cryptos)
        except ValueError:
            bot.send_message(message.chat.id, lang[13], reply_markup=cryptos)


def select_setting(message):
    lang = tlmanager.get_language(message.chat.id)
    if message.text == lang[2]:
        bot.send_message(message.chat.id, lang[3], reply_markup=languages)
        bot.register_next_step_handler(message, set_language)
    elif message.text == lang[4]:
        bot.send_message(message.chat.id, lang[5], reply_markup=currencies)
        bot.register_next_step_handler(message, set_fiat_currency)
    elif message.text == lang[16]:
        bot.send_message(message.chat.id, lang[17], reply_markup=themes)
        bot.register_next_step_handler(message, set_theme)
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


def set_theme(message):
    lang = tlmanager.get_language(message.chat.id)
    if message.text in thememanager.themes.keys():
        theme = message.text
        dbmanager.set_data(message.chat.id, "theme", theme)
        # Notify user that his default fiat currency was changed
        bot.send_message(message.chat.id, f"{lang[18][0]}{theme}{lang[18][1]}", reply_markup=cryptos)
    else:
        # Notify user that his default fiat currency was NOT changed
        bot.send_message(message.chat.id, lang[6], reply_markup=cryptos)


def set_language(message):
    if config.supported_languages[message.text]:
        dbmanager.set_data(message.chat.id, "language", config.supported_languages[message.text])
        # Notify user that his default fiat currency was changed
        bot.send_message(message.chat.id, tlmanager.languages[config.supported_languages[message.text]][7],
                         reply_markup=cryptos)


# Handler for text messages received from users
@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    text = message.text  # Get the text message from the user
    currency = dbmanager.get_data(message.chat.id, "currency", "usd")  # Get user's default fiat currency
    lang = tlmanager.get_language(message.chat.id)
    data = cgapimanager.get_crypto_price(text,
                                         currency, True)
    # Call get_crypto_price function to get the cryptocurrency data

    # Extract cryptocurrency ID and USD price and other data from the list
    coin = data[0]
    price = data[1]

    market_cap = data[2]
    volume = data[3]
    percent_change = data[4]

    timestamps = data[5]
    prices = data[6]

    graph = graphmanager.generate_price_change_graph(timestamps, prices, percent_change > 0, message.chat.id, lang)

    # Send the cryptocurrency price to the user
    reply = (f"{lang[8][0]}{coin}{lang[8][1]}{price:.2f}{currency}{lang[8][2]}\n"
             f"{lang[10][0]}{market_cap}{currency}{lang[10][1]}\n"
             f"{lang[11]}{volume}{currency}\n"
             f"{lang[12][0]}{percent_change}%{lang[12][1]}")
    bot.send_photo(message.chat.id, photo=open(graph, "rb"), caption=reply, reply_markup=cryptos)
    os.remove(graph)


# Start the bot
bot.infinity_polling()
