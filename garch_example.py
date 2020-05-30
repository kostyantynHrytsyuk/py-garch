from api_wrap import ApiWrapper
from garch import MyGARCH
from stock import Stock

# Load prices for S&P 500 index
sp500prices = ApiWrapper.load_prices_json('%5EGSPC')

sp500 = Stock(sp500prices)

sp500_returns = sp500.calculate_returns()

# Make an instance of class MyGARCH
garch = MyGARCH(sp500_returns)

# Get GARCH model for S&P500
model = garch.get_garch_model()
