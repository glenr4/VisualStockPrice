import file_handling as fh

# Input variables used across the codebase
stockSymbol = "GC"
interval = '1d'

# If downloading data, set the start and end dates
startDate = '2025-01-01'
endDate = '2025-02-19'

# Price movement
large_move_max_candles=5
large_move_threshold_percent=4
pre_large_move_candles=50


# Yahoo finance symbols
# "^AORD" # Australian All Ordinaries Index