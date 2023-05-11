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

## License

CryptoPriceBot is licensed under the MIT License. See `LICENSE` for more information.
