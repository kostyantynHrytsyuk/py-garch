from arch import arch_model
import pandas as pd
import matplotlib.pyplot as plt


class MyGARCH:
    """
    Class for GARCH(1,1) modeling
    """
    def __init__(self, returns, dates):
        self.arr = pd.DataFrame(data=returns,
                                columns=['Return'],
                                index=dates)
        self.fit = None

    def get_garch_model(self):
        return arch_model(self.arr['Return']*10, p=1, q=1,
                          mean='constant', vol='GARCH', dist='normal')

    def fit_garch(self, model, upd_freq=4):
        self.fit = model.fit(update_freq=upd_freq, disp='off')
        return self.fit

    def show_fit_result(self):
        assert self.fit, "There is no fitted model!"
        self.fit.plot()
        plt.show()

    def get_forecast(self, horizon=10):
        forecast = self.fit.forecast(horizon=horizon)
        return forecast.variance[-1:].transpose() / 100

    def predict_volatility(self):
        """
        Predicts volatility with GARCH model
        """
        model = self.get_garch_model()
        self.fit_garch(model)
        self.show_fit_result()
        forecast = self.get_forecast()
        MyGARCH.print_forecast(forecast)

    @staticmethod
    def print_forecast(f):
        """

        """
        print("\nPrediction of volatility since " + str(sorted(f)[0]) + " for " + str(len(f)) + " days")
        print(f)
