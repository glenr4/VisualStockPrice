# https://ranaroussi.github.io/yfinance/reference/yfinance.price_history.html

import yfinance as yf
import mplfinance as mpf
import os
import pandas as pd

# variables
source_file = "./data/GC=F_2024-01-01_2024-12-31.csv"

# Create sub-folders
if not os.path.exists("data"):
    os.mkdir("data")
if not os.path.exists("images"):
    os.mkdir("images")

# Load the stock data from the saved CSV file
df = pd.read_csv(source_file, index_col=0, parse_dates=True)

# Create the candlestick chart using mplfinance
chart_style = mpf.make_mpf_style(base_mpf_style='classic', gridstyle='')
mpf.plot(df, type='candle', style=chart_style, axisoff=True,  volume=False, savefig='aapl_candlestick.png')