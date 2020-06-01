from arrays import ArrayDateIndex
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
        querystring = {"symbol": company_sym, "interval": "1d", "range": "max"}
        p_json = ApiWrapper.execute_request("stock/v2/get-chart", querystring)

        dates, prices = ApiWrapper.__extract_data_from_price_json(p_json)
        prices, dates = Utils.remove_none_in_two_lists(prices, dates)
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
