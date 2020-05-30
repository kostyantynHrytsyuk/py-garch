import yfinance as yf
from arch import arch_model


class MyGARCH:
    """
    Class for GARCH(1,1) modeling
    """
    def __init__(self, returns):
        self.arr = returns

    def get_garch_model(self):
        return arch_model(self.arr, p=1, q=1,
                          mean='constant', vol='GARCH', dist='normal')

#vti = yf.Ticker('VTI')
#h_ap = aapl.history(period='max')
# Get prices
#vti_close_price = vti.history(start='2001-06-18', end='2020-05-08')['Close']
# Calculate returns
#vti_returns = vti_close_price.shift(1) / vti_close_price - 1
# Calculate volatility
#appl_sd = vti_returns.rolling(22).std()
