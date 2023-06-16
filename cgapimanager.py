import pycoingecko

# Initialize CoinGeckoAPI object
cg = pycoingecko.CoinGeckoAPI()


# Function to fetch the cryptocurrency price
def get_crypto_price(coin: str, currency: str, get_additional_info: bool):
    coin_id = cg.search(coin)["coins"][0]["id"]  # Search the coin on CoinGecko API and get its ID

    currency = currency.lower()
    crypto_data = cg.get_price(ids=coin_id, vs_currencies=currency)
    # Fetch the price data for the specified cryptocurrency

    price = crypto_data[coin_id][currency]  # Get default fiat currency price for the specified cryptocurrency
    if not get_additional_info:
        return price

    coin_data = cg.get_coin_by_id(id=coin_id)
    market_data = coin_data['market_data']
    market_cap = market_data['market_cap'][currency]  # Market capitalization in USD
    volume = market_data['total_volume'][currency]  # Trading volume in USD
    percent_change_24h = market_data['price_change_percentage_24h']  # Percentage change in price in the last 24 hours
    # You can fetch other market data fields similarly

    return [coin_id, price, market_cap, volume,
            percent_change_24h]  # Return the cryptocurrency ID and default fiat currency price in a list


def perform_currency_conversion(amount: int, from_curr: str, to_curr: str):
    coins = [x["symbol"] for x in cg.get_coins_list()]
    vs_currs = cg.get_supported_vs_currencies()

    if from_curr in coins and to_curr in coins:
        from_curr_usd_price = get_crypto_price(from_curr, "usd", False)
        to_curr_usd_price = get_crypto_price(to_curr, "usd", False)
        conversion_rate = from_curr_usd_price / to_curr_usd_price

    elif from_curr in coins and to_curr in vs_currs:
        conversion_rate = get_crypto_price(from_curr, to_curr, False)

    elif from_curr in vs_currs and to_curr in coins:
        conversion_rate = 1 / get_crypto_price(to_curr, from_curr, False)

    elif from_curr in vs_currs and to_curr in vs_currs:
        from_curr_usdt_price = get_crypto_price("usdt", from_curr, False)
        to_curr_usdt_price = get_crypto_price("usdt", to_curr, False)
        conversion_rate = to_curr_usdt_price / from_curr_usdt_price

    else:
        return "error"

    return amount * conversion_rate
