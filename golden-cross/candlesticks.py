"""
candlesticks.py
Author: Carl Barcenas
Contains functions related to obtaining candlestick trends
"""
import robin_stocks as r
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# DELETETHIS
password = input("Enter your password: ")
r.login('carlbarcenas95@gmail.com', password)


def check_up_down(data):  # FIXTHIS
    """
    Checks if the data trend is up or down based on derivative of the data.
    NOTE: This only checks for a trend in the past week and turns it into
    a linear equation, thus it may not be completely accurate in every situation

    Returns:
        1 if uptrend
        0 if stable
        -1 if downtrend
    """
    np_data = np.array(data).astype('float')
    np_data_week = np_data[-8:-1]
    t = np.arange(-7, 0)
    z = np.polyfit(t, np_data_week, 1)
    plt.plot(t, np_data_week)
    plt.show()

    if z[0] > 0:
        return 1
    elif z[0] < 0:
        return -1
    else:
        return 0


def find_hammer(ticker):
    """
    Find if the data presented shows a hammer indicator within the past 3 days.

    """
    # Define Data
    data = pd.DataFrame(r.get_historicals(ticker, span='year', bounds='regular'))
    np_open = np.array(data['open_price']).astype('float')
    np_close = np.array(data['close_price']).astype('float')
    np_high = np.array(data['high_price']).astype('float')
    np_low = np.array(data['low_price']).astype('float')

    # Check for downtrend
    if check_up_down(np_close) != -1:
        print("No downtrend history, thus no hammer.")
        return

    n = -1

    while n >= -3:
        # Check bearish or bullish
        if np_open[n] < np_close[n]:
            bullish = True
        else:
            bullish = False

        # Define candlestick real body and shadow length
        real_body = abs(np_open[n] - np_close[n])
        if bullish:
            upper_shadow = np_high[n] - np_open[n]
            lower_shadow = np_close[n] - np_low[n]
        else:
            upper_shadow = np_high[n] - np_close[n]
            lower_shadow = np_open[n] - np_low[n]

        n -= 1

        # Define hammer candlestick ratios in percentages
        up_ratio = 0.05
        rb_ratio = 0.3167
        low_ratio = 0.6334

        # Check hammer requirements
        total = real_body + upper_shadow + lower_shadow
        if up_ratio <= upper_shadow / total and \
                rb_ratio <= real_body / total and \
                low_ratio <= lower_shadow / total:
            print("Hammer")


find_hammer('JOBS')
