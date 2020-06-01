from stock import Stock
from garch import MyGARCH

if __name__ == '__main__':
    # Load prices for S&P 500 index
    sp500 = Stock.get_company_info('%5EGSPC')
    sp500.plot_returns()

    # Make an instance of class MyGARCH
    garch = MyGARCH(sp500.rets, sp500.get_indices())

    # Get GARCH model prediction for S&P500
    garch.predict_volatility()
