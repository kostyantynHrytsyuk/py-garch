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

    def calculate_returns(self):
        """
        Calculate returns for stock
        Price - name of the column
        """
        rets = []
        for i in range(len(self.arr)-1):
            r = (self.arr[i+1]-self.arr[i])/self.arr[i]
            rets.append(r)
        return rets

    def calculate_volatility(self, scale=1):
        """
        Calculate volatility and scale it
        :param scale:
        1 - daily volatility
        21 - monthly volatility
        252 - annual volatility
        """
        z = statistics.stdev(self.calculate_returns()) * math.sqrt(scale)
        return z

    def plot_returns(self):
        plt.plot(self.calculate_returns())
        plt.show()