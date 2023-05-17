# CryptoPriceBot
CryptoPriceBot is a Telegram bot that provides real-time cryptocurrency price data from CoinGecko API. It is built with Python and the Telebot library.

## Usage
You can find running instance of this bot [here](https://t.me/cryptOwObot).

## Setup
To create your own instance of CryptoPriceBot, follow these steps:
1. Clone this repository:
```
git clone https://github.com/L1S69/CryptoPriceBot.git
cd CryptoPriceBot
```
2. Activate virtual environment:
```
source env/bin/activate
```
3. If you don't have `SQLite3` installed, install it. For example, in Arch Linux it's done like this:
```
sudo pacman -S sqlite3
```
4. Create a Telegram bot and set its token in the `config.py` file. You can obtain a token by talking to the [BotFather](https://t.me/BotFather) on Telegram.

5. Run the bot:
```
python bot.py
```
6. Open Telegram and start a chat with your bot. Select a cryptocurrency from the custom keyboard or type it manually to get its latest price data.

## Contributions

We welcome contributions from the community. If you find a bug or have a feature request, please open an issue on this repository. Pull requests are also welcome.

## Translations

To make a custom translation for your Telegram bot, follow these steps:

1. Locate the `translations/` directory in your project.
2. Copy any existing JSON file in the `translations/` directory. The JSON file represents the language translation for your bot.
3. Rename the copied file to the desired language code. For example, if you want to create a translation for French, you can name it `fr.json`.
4. Open the copied JSON file with a text editor.
5. Translate the phrases and messages in the file to the desired language.
6. Save the file with the translated phrases.
7. Open the `config.py` file in your project.
8. Locate the `supported_languages` dictionary in the `config.py` file.
9. Add an entry for your newly created language code and specify the language name as the key. For example, if you added a translation for French, you can add `"🇫🇷French": "fr"` to the `supported_languages` dictionary.
10. Save the `config.py` file.

Once you have completed these steps, your bot will be able to use the custom translation for the specified language. You can now set the newly added language as the default language for your bot or allow users to select it using the available language selection functionality.

## License

CryptoPriceBot is licensed under the MIT License. See `LICENSE` for more information.
