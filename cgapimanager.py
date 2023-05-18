from pycoingecko import CoinGeckoAPI # Library for fetching crypto price data


# Initialize CoinGeckoAPI object
cg = CoinGeckoAPI()

# Function to fetch the cryptocurrency price
def get_crypto_price(coin: str, currency: str):
    id = cg.search(coin)["coins"][0]["id"] # Search the coin on CoinGecko API and get its ID
    
    currency = currency.lower()
    crypto_data = cg.get_price(ids=id, vs_currencies=currency) # Fetch the price data for the specified cryptocurrency
    price = crypto_data[id][currency] # Get default fiat currency price for the specified cryptocurrency

    coin_data = cg.get_coin_by_id(id=id)
    market_data = coin_data['market_data']
    market_cap = market_data['market_cap'][currency]  # Market capitalization in USD
    volume = market_data['total_volume'][currency]  # Trading volume in USD
    percent_change_24h = market_data['price_change_percentage_24h']  # Percentage change in price in the last 24 hours
    # You can fetch other market data fields similarly
    
    return [id, price, market_cap, volume, percent_change_24h] # Return the cryptocurrency ID and default fiat currency price in a list 
