import numpy as np
import pandas as pd
import yfinance as yf
import datetime

fx = ['EUR','GBP','USD','CAD','JPY']

def get_fx_data(currency):
	ans = _get_fx_prices(currency)
	getdollars = _get_fx_prices("GBP").reindex(ans.index, method="ffill")
	ans = ans / getdollars
	return ans

def _get_fx_prices(currency):
	if currency == "USD":
		date_range = pd.date_range(datetime.datetime(2003, 12, 1), datetime.datetime.now())
		forex_data = pd.DataFrame({"Value": [1.0] * len(date_range), "Date": date_range}).set_index('Date')
	else:
		forex_data = yf.download(currency+'USD=X', start='2003-12-01', end=datetime.datetime.now())
		forex_data = forex_data[['Close']]
		forex_data.columns = [col[0] for col in forex_data.columns]
		forex_data = forex_data.rename(columns={'Close':'Value'}).tz_localize(None)
	return forex_data

data=_get_fx_prices(fx[0])
data.to_csv('data.csv') # currency value in USD
result = get_fx_data(fx[2])
result.to_csv('result.csv') # currency value in GBP