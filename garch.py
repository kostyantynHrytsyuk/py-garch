import yfinance as yf

vti = yf.Ticker('VTI')
#h_ap = aapl.history(period='max')
# Get prices
vti_close_price = vti.history(start='2001-06-18', end='2020-05-08')['Close']
# Calculate returns
vti_returns = vti_close_price.shift(1) / vti_close_price - 1
# Calculate volatility
appl_sd = vti_returns.rolling(22).std()
