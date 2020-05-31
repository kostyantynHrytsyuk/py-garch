from api_wrap import ApiWrapper
from garch import MyGARCH

# Load prices for S&P 500 index
sp500 = ApiWrapper.get_company_info('%5EGSPC')
sp500.calculate_volatility()
sp500.plot_returns()

# Make an instance of class MyGARCH
garch = MyGARCH(sp500.rets, sp500.get_indices())

# Get GARCH model prediction for S&P500
garch.predict_volatility()
