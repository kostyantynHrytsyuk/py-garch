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

    # def test_info_getting(self):
    #    self.assertEqual(self.stock, Stock(self.company))


if __name__ == '__main__':
    unittest.main()
