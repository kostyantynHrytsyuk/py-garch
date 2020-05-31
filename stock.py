from arrays import ArrayDateIndex
import math
import matplotlib.pyplot as plt
import statistics


class Stock:
    """
    Class for calculating stock statistic metrics
    """
    def __init__(self, arr):
        """
        :param arr: instance of ArrayDateIndex with prices of stock
        """
        assert type(arr) == ArrayDateIndex, 'Wrong array type!'
        self.arr = arr
        self.rets = None
        self._mean = None

    @property
    def mean(self):
        if not self.mean:
            self.mean = statistics.mean(self.rets)
        return self.mean

    @mean.setter
    def mean(self, x):
        self.mean = x

    def calculate_returns(self):
        """ () -> list
        Calculate returns for stock
        Price - name of the column
        """
        if not self.rets:
            rets = []
            for i in range(len(self.arr)-1):
                r = (self.arr[i+1]-self.arr[i])/self.arr[i]
                rets.append(r)
            self.rets = rets
        return self.rets

    def calculate_volatility(self, scale=1):
        """ (int) -> int
        Calculate volatility and scale it
        :param scale:
        1 - daily volatility
        21 - monthly volatility
        252 - annual volatility
        """
        z = statistics.stdev(self.calculate_returns()) * math.sqrt(scale)
        return z

    def get_sharpe_ratio(self, scale=1):
        """ (int) -> int
        Return the basic finance metric Sharpe ratio
        """
        return self.mean/self.calculate_volatility(scale)

    def plot_returns(self):
        plt.plot(self.calculate_returns())
        plt.show()
