from api_wrap import ApiWrapper

# Load prices for S&P 500 index
sp500 = ApiWrapper.load_prices_json('%5EGSPC')
