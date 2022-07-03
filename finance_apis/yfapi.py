import requests
from secret import yfapi_key
api_key = yfapi_key

# quote_url = "https://yfapi.net/v6/finance/quote"

# querystring = {"symbols": "^SP500TR,^DJI,NDAQ,BTC-USD,EURUSD=X"}

# headers = {
#     'x-api-key': api_key
# }

# response = requests.request(
#     "GET", quote_url, headers=headers, params=querystring)

# print(response.text)

# quote_url = "https://yfapi.net/v6/finance/quote"
options_url = "https://yfapi.net/v7/finance/options"
quote_summary_url = "https://yfapi.net/v11/quoteSummary"
chart_data_url = "https://yfapi.net/v8/finance/chart"
similar_stocks_url = "https://yfapi.net/v6/finance/recommendationsbysymbol"
most_watched_url = "https://yfapi.net/ws/screeners/v1/finance/screener/predefined/saved"
insights_url = "https://yfapi.net/ws/insights/v1/finance/insights"
autocomplete_url = "https://yfapi.net/v6/finance/autocomplete"
market_summary_url = "https://yfapi.net/v6/finance/quote/marketSummary"
trending_stocks_by_region_url = "https://yfapi.net/v6/finance/quote/marketSummary"


# /v6/finance/quote - real time quote data for stocks, ETFs, mutuals funds, bonds, crypto and national currencies.
# /v7/finance/options - option chains data for a particular stock market company
# /v8/finance/spark - historical data for various intervals and ranges
# /v11/finance/quoteSummary - very detailed information for a particular ticker symbol
# /v8/finance/chart - chart data
# /v6/finance/recommendationsbysymbol - list of similar stocks
# /ws/screeners/v1/finance/screener/predefined/saved - list of most added stocks to the watchlist
# /ws/insights/v1/finance/insights - research insights
# /v6/finance/autocomplete - auto complete stock suggestions
# /v6/finance/quote/marketSummary - live market summary information at the request time
# /v1/finance/trending - trending stocks in a specific region

# market_response = requests.request(
#     "GET", market_summary_url, headers={'x-api-key': api_key}, params={'US'})
# print(market_response.text)

query_string = "nasd"
autocomplete_response = requests.request(
    "GET", autocomplete_url, headers={'x-api-key': api_key}, params={'query': query_string, 'lang': 'en'})
print('$$$$%%%%AUTOCOMPLETE!!!!#########')
print(autocomplete_response.text)
