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
        self._rets = None
        self._mean = None

    @property
    def mean(self):
        if not self._mean:
            self._mean = statistics.mean(self.rets)
        return self._mean

    @mean.setter
    def mean(self, x):
        self._mean = x

    @property
    def rets(self):
        if not self._rets:
            self._rets = self.calculate_returns()
        return self._rets

    @rets.setter
    def rets(self, x):
        self._rets = x

    def calculate_returns(self):
        """ () -> list
        Calculate returns for stock
        Price - name of the column
        """
        if not self._rets:
            rets = []
            for i in range(len(self.arr)-1):
                r = (self.arr[i+1]-self.arr[i])/self.arr[i]
                rets.append(r)
            self._rets = rets
        return self.rets

    def calculate_volatility(self, scale=1):
        """ (int) -> int
        Calculate volatility and scale it
        :param scale:
        1 - daily volatility \n
        21 - monthly volatility \n
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

    def get_indices(self):
        return self.arr.get_indices()[1:]
