# https://ranaroussi.github.io/yfinance/reference/yfinance.price_history.html

import yfinance as yf
import mplfinance as mpf
import os
import pandas as pd
import var
import file_handling as fh

# TODO need to automatically pick symbol and interval from the file name
# stockSymbol = "GC"
# interval = '1d'

# TODO: for timeframes in minutes, include hours and minutes in the filename so that they don't get overwritten multiple times
# end_date.date()

large_move_max_candles = var.large_move_max_candles
large_move_threshold_percent = var.large_move_threshold_percent
pre_large_move_candles = var.pre_large_move_candles

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
  i = pre_move_window
  last_neutral_idx = -pre_move_window  # Track the last neutral image position

  while i < len(tickerDf) - window:
      start_date_pre_move = tickerDf.index[i - pre_move_window]
      start_date_move = tickerDf.index[i]
      end_date_move = tickerDf.index[i + window - 1]

      start_price = tickerDf['Close'][i]
      end_price = tickerDf['Close'][i + window - 1]
      pct_change = (end_price - start_price) / start_price * 100

      # Always capture the window for up/down moves
      pre_move_df = tickerDf[start_date_pre_move:start_date_move]
      
      # Capture the full move
      complete_window_df = tickerDf[start_date_pre_move:end_date_move]

      # For neutral moves, only capture if sufficiently spaced from last neutral
      if abs(pct_change) <= threshold_percent:
          if i - last_neutral_idx >= pre_move_window:
              large_moves.append((start_date_move, end_date_move, pre_move_df, pct_change, complete_window_df))
              last_neutral_idx = i
          i += 1
      else:
        #   print(f"Large move detected: {pct_change:.2f}% from {start_date_move.date()} to {end_date_move.date()}")
          large_moves.append((start_date_move, end_date_move, pre_move_df, pct_change, complete_window_df))
          i += window  # Move beyond the end of the large move

  return large_moves

# source_file = fh.browse_file('data')
input_dir = os.path.join(os.path.dirname(__file__), 'data')


for input_file in os.listdir(input_dir):
    if not input_file.endswith('.csv'):
        continue
        
    # source_file = os.path.join(input_dir, input_file)
    input_path = os.path.join(input_dir, input_file)

    stockSymbol = os.path.basename(input_file).split(' ')[0]

    # Create sub-folders
    for folder in ["data", "images", "images/up", "images/down", "images/neutral"]:
        if not os.path.exists(folder):
            os.makedirs(folder)


    # Load the stock data from the saved CSV file
    # input_file = './data/{}_{}_{}_{}.csv'.format(stockSymbol, startDate, endDate, interval)
    df = pd.read_csv(input_path, index_col=0, parse_dates=True)
    # print(df.head())
    # print(df.index[0])
    large_moves = find_large_price_moves(df, 
                                        window=large_move_max_candles, 
                                        threshold_percent=large_move_threshold_percent, 
                                        pre_move_window=pre_large_move_candles)

    # Create the candlestick chart using mplfinance
    chart_style = mpf.make_mpf_style(base_mpf_style='classic', gridstyle='')

    for start_date, end_date, window_df, pct_change, combined_window_df in large_moves:
    # Determine the directory based on the price movement
        if abs(pct_change) <= large_move_threshold_percent:
            direction = "neutral"
        elif pct_change > large_move_threshold_percent:
            direction = "up"
        else:
            direction = "down"

        print(f"Large move detected: {pct_change:.2f}% from {start_date.date()} to {end_date.date()}")


        # Image showing pre and post move
        filename = f"./images/{stockSymbol}_{start_date.date()}_{end_date.date()}_{var.interval}_pre{pre_large_move_candles}_post{large_move_max_candles}_pct{large_move_threshold_percent}_{direction}_full_move.png"
        mpf.plot(combined_window_df, type='candle', style=chart_style, axisoff=True, volume=False, savefig=filename)
        
        # Create filename with the percentage change included
        filename = f"./images/{direction}/{stockSymbol}_{start_date.date()}_{end_date.date()}_{var.interval}_pre{pre_large_move_candles}_post{large_move_max_candles}_pct{large_move_threshold_percent}_{direction}.png"
        
        # Plot only the pre-move candles
        mpf.plot(window_df, 
                    type='candle', 
                    style=chart_style, 
                    axisoff=True, 
                    volume=False, 
                    savefig=filename)
