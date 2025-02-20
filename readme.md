# Visual Stock Price Direction Predictor

## Setup

1. Install Python v3.13 or higher
1. Install Anaconda
1. Restore packages and create a new environment:

```sh
conda env create -n VisualStockPrice --file environment.yml
```

## Run It

### Input Parameters

Set in the `var.py` file.

### From a CLI:

```sh
python download_data.py
python generate_candles.py
python split_images.py
python train_model.py
python predict_price_move.py
```

# To do

- Create classes instead of stand alone files
