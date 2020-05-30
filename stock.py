from arrays import ArrayDateIndex
import math

class Stock:
    """
    Class for calculating stock statistic metrics
    """
    def __init__(self, arr):
        """
        :param arr: instance of ArrayDateIndex with prices of stock
        """
        assert type(arr) == ArrayDateIndex, 'Wrong array type!'
        self.arr = arr.to_pandas()

    def calculate_returns(self, col_name='Price'):
        """
        Calculate returns for stock
        Price - name of the column
        """
        return self.arr[col_name].pct_change()

    def calculate_volatility(self, scale=1):
        """
        Calculate volatility and scale it
        :param scale:
        1 - daily volatility
        21 - monthly volatility
        252 - annual volatility
        """
        return self.calculate_returns().std() * math.sqrt(scale)
