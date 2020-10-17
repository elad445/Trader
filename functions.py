from candlesticks import candlestick_patterns
import talib
import pandas as pd
import numpy as np
import yfinance as yf

class TA:

    def __init__(self):
        pass

    # this function inserts 2 columns to dataframe. stochastic fast/slow.
    def generate_stochastics(self, dataframe, slow, fast, days):
        info_tuple = talib._ta_lib.STOCH(dataframe["High"], dataframe["Low"], dataframe["Close"], slow, fast, 0, days, 0)
        # talib returns tuple with stoch. high and stoch. low. convert to np array and poach each tuple to insert to dataframe
        np.asarray(info_tuple)
        stoch_slow_list = info_tuple[0]
        stoch_fast_list = info_tuple[1]
        stoch_slow_list.index = dataframe.index
        stoch_fast_list.index = dataframe.index
        dataframe[f"St_{slow}"] = stoch_slow_list
        dataframe[f"St_{fast}"] = stoch_fast_list


    # def to determine if the stochastic has crossed the 20 line from bottem or crossed 80 from top.
    # function can signal change from each realm including change direction: x<20 <==> 20<x<80 <==> x>80
    # static - 3 options, change - 4 options. up down at, cross, 20 80 50 range.
    def stochastic_signal_test(self, stochastic_now, stochastic_last, lowbar, highbar):
        if lowbar < stochastic_last < highbar:
            if stochastic_now < lowbar:
                return "down_cross_20"
            elif stochastic_now > highbar:
                return "up_cross_80"
            else:
                return "at_50"
        elif lowbar > stochastic_last:
            if stochastic_now > lowbar:
                return "up_cross_20"
            else:
                return "at_20"
        elif highbar < stochastic_last:
            if stochastic_now < highbar:
                return "down_cross_80"
            else:
                return "at_80"


    # find uptrend or downtrend. x =  is bool for up or down trend. _x refers to the highest or lowest closing ref candle in sequence, i is the current candle in iteration
    def candle_sequence(self, dataframe):
        i = 0
        # create a list, to add to dataframe as added column with each candle data
        seq_list = []
        # assume initial trend to be up.
        is_uptrend = True
        high_ref_candle = dataframe.iloc[0, 2]
        low_ref_candle = dataframe.iloc[0, 3]
        close_ref_candle = dataframe.iloc[0, 4]
        # iterate over data frame. save the first candle as x and uptrend as true just for initial conditions
        for i in dataframe.index:

            high_current_candle = dataframe.iloc[i, 2]
            low_current_candle = dataframe.iloc[i, 3]
            close_current_candle = dataframe.iloc[i, 4]

            # if we're in uptrend and current (i) closes above lowest price of highest closing candle (x) in seq - seq continues
            # some candles are still in uptrend but fail to define the highest closing candle of sequence. if they do then redefine x
            if is_uptrend:
                if close_current_candle > low_ref_candle:
                    is_uptrend = True
                    if close_current_candle > close_ref_candle:
                        close_ref_candle = close_current_candle
                        high_ref_candle = high_current_candle
                        low_ref_candle = low_current_candle
                    seq_list.append("uptrend")
                elif close_current_candle < low_ref_candle:
                    is_uptrend = False
                    close_ref_candle = close_current_candle
                    low_ref_candle = low_current_candle
                    high_ref_candle = high_current_candle
                    seq_list.append("reverse to downtrend")
            # if we're in down seq and current (i) closes above highest price of lowest closing (x) candle in seq, seq reverse to up.
            # if current closes lower then highest_x of seq that's down, seq continues
            # if we're in an uptrend and current (i) closes lower then lowest price of highest closing candle (x) of seq, seq reverse to downtrend

            elif not is_uptrend:
                if close_current_candle > high_ref_candle:
                    # reversal
                    is_uptrend = True
                    close_ref_candle = close_current_candle
                    high_ref_candle = high_current_candle
                    low_ref_candle = low_current_candle
                    seq_list.append("reverse to uptrend")
                elif close_current_candle < high_ref_candle:
                    is_uptrend = False
                    if close_current_candle < close_ref_candle:
                        close_ref_candle = close_current_candle
                        low_ref_candle = low_current_candle
                        high_ref_candle = high_current_candle
                    seq_list.append("downtrend")
            else:
                seq_list.append("No data")
            i += 1
        column = pd.Series(seq_list)
        dataframe["Candle_seq"] = column.shift(1)
        return


    # this def signals for clean trends and possible crosses, false is for first 200 prices.
    # 1- uptrend -1 - downtrend, 0 - sideways, with exception to crosses, including output_str
    def moving_average_signals(self, current_ma20, current_ma50, current_ma200, current_tline):
        # dataframe cannot calc 200 sma for the first 200 prices of dataframe. need try and except to override error
        try:
            if current_tline > current_ma20 > current_ma50 > current_ma200:
                output_str = "bullish_clean"
                return 1, output_str
            elif current_tline < current_ma20 < current_ma50 < current_ma200:
                output_str = "bearish_clean"
                return -1, output_str
            else:
                if current_tline > current_ma20 > current_ma200 and current_ma50 > current_ma200:
                    output_str = "Possible bullish cross"
                    return 1, output_str
                elif current_ma200 > current_ma20 > current_tline and current_ma50 < current_ma200:
                    output_str = "possible bearish cross"
                    return -1, output_str
                else:
                    output_str = "sideways"
                    return 0, output_str
        except:
            return False


# function that tests for candlestick patterns returns a pattern name or null
# def to back-test a stock, (symbol df start end) capable of back-testing multiple symbols
# def to scan for stocks with the specified criteria (cs pattern, stoch, sma tline, trend)
# def is in trend?
# def match test - volume match, stochastic match, averages, trend


# back-test must include net worth at any given point. can make graph of total portfolio. (plot)
# back test should include closing of part of position


# strategy - classic trade:
#
# trends needs to be 1 or -1 clean
# volume_ok == True
# stochastic < 40 for long and > 60 for shorts
# candlestick sequence needs to be in direction. when reversed signal for potential trade in screener
#
# protocol 1 -
# candle seq match!
# trend sma is 1 or -1 clean
# candle seq reversed to trend direction
# volume_ok True
# stochastic < 40
# support and resistance lines shift, and trend is clear (fib?)
# candle pattern matches trade direction
# market is in same candle seq as trade direction in both timeframes
# price close above t_line for long and under for short signals
#
# getting out of p.1:
# if price closes below t_line
# elif price is twice as far as SL from tline, wait for close below tline_3 or hour chart candle close below tline
#
#
# protocol 2:
# candle seq match!
# stochastic doesn't matter!
# trends sma in direction 1 or -1 clean
# candle seq match to market
# volume ok true
# trend is clear in timeframe
