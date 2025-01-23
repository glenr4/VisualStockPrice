# https://ranaroussi.github.io/yfinance/reference/yfinance.price_history.html

import yfinance as yf
import mplfinance as mpf
import os
import pandas as pd

# Variables
stockSymbol = "GC=F"    # Gold futures
startDate = '2024-01-01'
endDate = '2024-12-31'
interval = '1d'

# Create sub-folders
if not os.path.exists("data"):
    os.mkdir("data")
if not os.path.exists("images"):
    os.mkdir("images")

# Load the stock data from the saved CSV file
source_file = './data/{}_{}_{}_{}.csv'.format(stockSymbol, startDate, endDate, interval)
df = pd.read_csv(source_file, index_col=0, parse_dates=True)

# Create the candlestick chart using mplfinance
chart_style = mpf.make_mpf_style(base_mpf_style='classic', gridstyle='')
mpf.plot(df, type='candle', style=chart_style, axisoff=True,  volume=False, savefig='aapl_candlestick.png')