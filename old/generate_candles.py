# Requires Kaleido to be installed using: pip install kaleido==0.1.0.post1

import pandas as pd
import plotly.graph_objects as go
import os


# variables
source_file = "./data/GC=F_2024-01-01_2024-12-31.csv"

# Create sub-folders
if not os.path.exists("data"):
    os.mkdir("data")
if not os.path.exists("images"):
    os.mkdir("images")

# Load the stock data from the saved CSV file
df = pd.read_csv(source_file, index_col=0, parse_dates=True)

# Step 2: Create the candlestick chart
fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name="Candlestick Chart"
)])

# Step 3: Customize chart layout (optional)
fig.update_layout(
    xaxis_rangeslider_visible=False  # Hide the range slider
)

fig.show()

# Step 4: Save the chart as a PNG file
fig.write_image("./images/candlestick_chart.png", width=500)
