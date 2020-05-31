from arch.univariate.mean import ConstantMean
from arrays import ArrayDateIndex
from api_wrap import ApiWrapper
from garch import MyGARCH
from stock import Stock
from utils import Utils
import datetime
import unittest


class MyTestGarch(unittest.TestCase):
    def setUp(self):
        # S&P 500
        self.company = ApiWrapper.load_prices_json('%5EGSPC')
        self.stock = ApiWrapper.get_company_info('%5EGSPC')
        self.response = ApiWrapper.execute_request('market/get-movers')
        self.garch = MyGARCH(self.stock.rets, self.stock.get_indices())

    def test_company_type(self):
        self.assertEqual(type(self.company), ArrayDateIndex)

    def test_index_type(self):
        self.assertEqual(type(self.company.get_indices()[0]), datetime.date)

    def test_indexing_in_ADT(self):
        self.assertRaises(AssertionError, self.company.__getitem__, -1)

    def test_check_names(self):
        self.assertRaises(KeyError, Utils.check_empty, self.response, 'wrong_key')

    def test_api_loading(self):
        self.assertEqual(type(self.response), dict)

    def test_info_getting(self):
        self.assertEqual(self.stock.mean, Stock(self.company).mean)

    def test_volatility_calculations(self):
        expected = [0.10749645873578462,
                    0.4926106590964299,
                    1.706453379810017]
        actual = [self.stock.calculate_volatility(),
                  self.stock.calculate_volatility(21),
                  self.stock.calculate_volatility(252)]
        self.assertEqual(actual, expected)

    def test_indices_equality(self):
        self.assertEqual(self.company.get_indices()[1:], self.stock.get_indices())

    def test_sharpe_ratio(self):
        self.assertAlmostEqual(round(self.stock.get_sharpe_ratio(), 4), 0.1826)

    def test_arch_model_type(self):
        self.assertEqual(type(self.garch.get_garch_model()), ConstantMean)

    def test_garch_fit(self):
        self.garch.fit_garch(self.garch.get_garch_model())
        self.assertIsNotNone(self.garch.fit)

    def test_forecast_horizon(self):
        horizon = 7
        self.garch.fit_garch(self.garch.get_garch_model())
        forecast = self.garch.get_forecast(horizon)
        self.assertEqual(horizon, len(forecast))


if __name__ == '__main__':
    unittest.main()
