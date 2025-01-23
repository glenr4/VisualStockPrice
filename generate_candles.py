# https://ranaroussi.github.io/yfinance/reference/yfinance.price_history.html

import yfinance as yf
import mplfinance as mpf
import os
import pandas as pd

# Variables
stockSymbol = "GC=F"    # Gold futures
startDate = '2015-01-01'
endDate = '2024-12-31'
interval = '1d'
large_move_max_candles=5
large_move_threshold_percent=4
pre_large_move_candles=50

# Create sub-folders
if not os.path.exists("data"):
    os.mkdir("data")
if not os.path.exists("images"):
    os.mkdir("images")

def find_large_price_moves(tickerDf, window=5, threshold_percent=4, pre_move_window=30):
  """
  Finds price moves within the given DataFrame that are greater than the specified threshold 
  over the given window size and captures the preceding 'pre_move_window' candles. 
  Moves beyond the end of a detected large move before searching for the next one.

  Args:
    tickerDf: DataFrame containing stock data with 'Open', 'High', 'Low', 'Close' columns.
    window: Number of candles (days) to consider for the price move calculation.
    threshold: Percentage threshold for price movement.
    pre_move_window: Number of candles to capture before the large move.

  Returns:
    A list of tuples, where each tuple contains:
      - Start date of the pre-move window
      - End date of the move window
      - Percentage price change over the move window
      - DataFrame containing the stock data within the combined window
  """

  large_moves = []
  i = pre_move_window  # Start from pre_move_window

  while i < len(tickerDf) - window:
    start_date_pre_move = tickerDf.index[i - pre_move_window]
    start_date_move = tickerDf.index[i]
    end_date_move = tickerDf.index[i + window - 1]

    start_price = tickerDf['Close'][i]
    end_price = tickerDf['Close'][i + window - 1]
    pct_change = (end_price - start_price) / start_price * 100

    if abs(pct_change) > threshold_percent:
      combined_window_df = tickerDf[start_date_pre_move:end_date_move]
      large_moves.append((start_date_move, end_date_move, combined_window_df))
      i += window  # Move beyond the end of the large move
    else:
      i += 1

  return large_moves

# Load the stock data from the saved CSV file
source_file = './data/{}_{}_{}_{}.csv'.format(stockSymbol, startDate, endDate, interval)
df = pd.read_csv(source_file, index_col=0, parse_dates=True)

large_moves = find_large_price_moves(df, 
                                     window=large_move_max_candles, 
                                     threshold_percent=large_move_threshold_percent, 
                                     pre_move_window=pre_large_move_candles)

# Create the candlestick chart using mplfinance
chart_style = mpf.make_mpf_style(base_mpf_style='classic', gridstyle='')

for start_date, end_date, window_df in large_moves:
  filename = f"./images/large_move_{start_date.date()}_{end_date.date()}_{pre_large_move_candles}.png"
  mpf.plot(window_df, type='candle', style=chart_style, axisoff=True,  volume=False, savefig=filename)
