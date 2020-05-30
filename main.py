import datetime
import json
import requests
from arrays import ArrayDateIndex

def return_movers(move):
    result = check_empty(check_empty(move, 'finance'), 'result')
    companies = []
    for r in result:
        quotes = check_empty(r, 'quotes')
        symbols = extract_symbols_from_quotes(quotes)
        companies.extend(symbols)
    return companies


def extract_symbols_from_quotes(quotes):
    symbols = []
    for q in quotes:
        s = check_empty(q, 'symbol')
        symbols.append(s)
    return symbols


def check_empty(d, key_name):
    r = d.get(key_name)
    if r:
        return r
    else:
        raise Exception('Empty field' + key_name)


def load_prices_json(company_sym, url, headers):
    querystring = {"interval": "1d", "region": "US", "symbol": company_sym, "lang": "en", "range": "max"}

    response = requests.request("GET", url+"stock/v2/get-chart", headers=headers, params=querystring)
    return json.loads(response.text)


def extract_data_from_price_json(p_json):
    ts = check_empty(check_empty(p_json, 'chart'), 'result')[0]
    # Dates
    date_stamps = convert_timestamps_to_date(ts)

    # Close prices
    close_prices = extract_close_prices(ts)
    return date_stamps, close_prices


def convert_timestamps_to_date(ts):
    date_stamps = []
    for stamp in check_empty(ts, 'timestamp'):
        date_stamps.append(datetime.datetime.fromtimestamp(stamp).date())
    return date_stamps


def extract_close_prices(ts):
    indicators = check_empty(ts, 'indicators')
    quotes = check_empty(indicators, 'quote')
    close = check_empty(quotes[0], 'close')
    return close


url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/"

querystring = {"region": "US", "lang": "en"}

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "4fbad8d46fmshbfd2331f0b71454p101088jsnd44f285321ff"
    }

response = requests.request("GET", url+"market/get-movers", headers=headers, params=querystring)

x = response.text
comp = return_movers(json.loads(x))

stock = extract_data_from_price_json(load_prices_json(comp[0], url, headers))
# stock = extract_data_from_price_json(load_prices_json('VTI', url, headers))

arr = ArrayDateIndex(len(stock[0]), stock[0], stock[1])

print(arr[5])
print(arr[datetime.date(2018, 4, 16)])
print(arr[datetime.date(2020, 4, 27)])

print()
