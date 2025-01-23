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

def find_large_price_moves(tickerDf, window=5, threshold=0.05):
  """
  Finds price moves within the given DataFrame that are greater than the specified threshold 
  over the given window size.

  Args:
    tickerDf: DataFrame containing stock data with 'Close' column.
    window: Number of candles (days) to consider for the price move calculation.
    threshold: Percentage threshold for price movement.

  Returns:
    A list of tuples, where each tuple contains:
      - Start date of the window
      - End date of the window
      - Percentage price change over the window
  """

  large_moves = []
  for i in range(len(tickerDf) - window + 1):
    start_date = tickerDf.index[i]
    end_date = tickerDf.index[i + window - 1]
    start_price = tickerDf['Close'][i]
    end_price = tickerDf['Close'][i + window - 1]
    pct_change = (end_price - start_price) / start_price

    if abs(pct_change) > threshold:
      window_df = tickerDf[start_date:end_date]
      large_moves.append((start_date, end_date, window_df))

  return large_moves

# Load the stock data from the saved CSV file
source_file = './data/{}_{}_{}_{}.csv'.format(stockSymbol, startDate, endDate, interval)
df = pd.read_csv(source_file, index_col=0, parse_dates=True)

large_moves = find_large_price_moves(df, window=5, threshold=0.03)

# Create the candlestick chart using mplfinance
chart_style = mpf.make_mpf_style(base_mpf_style='classic', gridstyle='')

for start_date, end_date, window_df in large_moves:
  filename = f"./images/large_move_{start_date.date()}_{end_date.date()}.png"
  mpf.plot(window_df, type='candle', style=chart_style, axisoff=True,  volume=False, savefig=filename)
