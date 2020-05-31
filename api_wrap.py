from arrays import ArrayDateIndex
from stock import Stock
from utils import Utils
import json
import requests


class ApiWrapper:
    URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/"
    querystring = {"region": "US", "lang": "en"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "4fbad8d46fmshbfd2331f0b71454p101088jsnd44f285321ff"
    }

    @classmethod
    def execute_request(cls, endpoint, query=None):
        if query:
            query.update(ApiWrapper.querystring)
        else:
            query = ApiWrapper.querystring
        url = ApiWrapper.URL + endpoint
        response = requests.request("GET",
                                    url,
                                    headers=ApiWrapper.headers,
                                    params=query)

        return json.loads(response.text)

    @classmethod
    def get_movers(cls):
        move = cls.execute_request("market/get-movers")
        result = Utils.check_empty(Utils.check_empty(move, 'finance'), 'result')
        companies = []
        for r in result:
            quotes = Utils.check_empty(r, 'quotes')
            symbols = cls.extract_symbols_from_quotes(quotes)
            companies.extend(symbols)
        return companies

    @classmethod
    def extract_symbols_from_quotes(cls, quotes):
        symbols = []
        for q in quotes:
            s = Utils.check_empty(q, 'symbol')
            symbols.append(s)
        return symbols

    @classmethod
    def load_prices_json(cls, company_sym):
        querystring = {"symbol": company_sym, "interval":"1d", "range": "max"}
        p_json = ApiWrapper.execute_request("stock/v2/get-chart", querystring)

        dates, prices = ApiWrapper.__extract_data_from_price_json(p_json)
        return ArrayDateIndex(len(prices), dates, prices)

    @classmethod
    def __extract_close_prices(cls, ts):
        indicators = Utils.check_empty(ts, 'indicators')
        quotes = Utils.check_empty(indicators, 'quote')
        close = Utils.check_empty(quotes[0], 'close')
        return close

    @classmethod
    def __extract_data_from_price_json(cls, p_json):
        ts = Utils.check_empty(
            Utils.check_empty(p_json, 'chart'), 'result')[0]
        # Dates
        date_stamps = Utils.convert_timestamps_to_date(ts)

        # Close prices
        close_prices = ApiWrapper.__extract_close_prices(ts)
        return date_stamps, close_prices

    @classmethod
    def get_company_info(cls, sym):
        company = cls.execute_request('stock/v2/get-profile', query={"symbol": "F"})
        info = Utils.check_empty(company, 'quoteType')
        print('\nCompany: ' + Utils.check_empty(info, 'longName'))
        print('\nStock exchange: ' + Utils.check_empty(info, 'exchange'))
        print('\nMarket: ' + Utils.check_empty(info, 'market'))

        stock = Stock(cls.load_prices_json(sym))

        print('\nAverage return: ' + str(round(stock.mean, 4)))
        print('\nDaily volatility: ' + str(round(stock.calculate_volatility(), 4)))
        print('\nMonthly volatility: ' + str(round(stock.calculate_volatility(21), 4)))
        print('\nAnnual volatility: ' + str(round(stock.calculate_volatility(252), 4)))
        print('\nSharpe ratio: ' + str(round(stock.get_sharpe_ratio(), 4)))

        return stock
