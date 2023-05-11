from pycoingecko import CoinGeckoAPI # Library for fetching crypto price data


# Initialize CoinGeckoAPI object
cg = CoinGeckoAPI()

# Function to fetch the cryptocurrency price
def get_crypto_price(coin: str, currency: str):
    id = cg.search(coin)["coins"][0]["id"] # Search the coin on CoinGecko API and get its ID
    
    currency = currency.lower()
    crypto_data = cg.get_price(ids=id, vs_currencies=currency) # Fetch the price data for the specified cryptocurrency
    price = crypto_data[id][currency] # Get default fiat currency price for the specified cryptocurrency
    
    return [id, price] # Return the cryptocurrency ID and default fiat currency price in a list 
