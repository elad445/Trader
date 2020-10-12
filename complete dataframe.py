import numpy as np
import pandas as pd
import talib
import yfinance as yf
from functions import TA

ticker = "SPY"
data = yf.download(ticker, start="2020-08-01")
# add int index to dataframe ==>
data.reset_index(inplace=True)

# add columns with data to df.
data["T_3"] = talib.EMA(data["Adj Close"], timeperiod=3)
data["T_Line"] = talib.EMA(data["Adj Close"], timeperiod=8)
data["MA_20"] = talib.SMA(data['Adj Close'], 20)
data["MA_50"] = talib.SMA(data['Adj Close'], 50)
data["MA_200"] = talib.SMA(data['Adj Close'], 200)
TA.generate_stochastics(TA, data, 12, 3, 3)
TA.candle_sequence(TA, data)
# 0-date  1-open  2-high  3-low  4-close  5-adj  6-vol  7-t_3  8-t_line  9-ma_20  10-ma_50 11-ma_200  12-st_12  13-st_3  14-candle_seq


# back-testing ==>
