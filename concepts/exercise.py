import numpy as np
import pandas as pd

ma = pd.read_csv("../data/moving-average-exercise.csv")
ma.info()
ma.head(n=10)

# both columns have Dtype object 
ma['Date'] = pd.to_datetime(ma.Date, errors='raise') # convert to date
ma['Sales'] = ma['Sales'].str.replace(",", "") # replace commas
ma['Sales'] = pd.to_numeric(ma.Sales, errors='raise') # convert to numeric

ma.info()
ma.describe()

# rolling mean
ma['ma_7'] = ma['Sales'].rolling(window=7).mean().round()
ma['ma_14'] = ma['Sales'].rolling(window=14).mean().round()

ma[ma['Date'].astype(str).str.contains('2009-01')] # January
ma[ma['Date'].astype(str).str.contains('^2009-03')] # March
# for a specific date
ma.query('Date == "2009-03-19"') # or ma[ma['Date'] == '2009-03-19']