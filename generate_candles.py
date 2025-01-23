import yfinance as yf
import mplfinance as mpf

# Download historical data for a specific stock (e.g., Apple)
tickerSymbol = 'AAPL'
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1mo') 

# Create the candlestick chart using mplfinance
chart_style = mpf.make_mpf_style(base_mpf_style='classic', gridstyle='')
mpf.plot(tickerDf, type='candle', style=chart_style, axisoff=True,  volume=False, savefig='aapl_candlestick.png')