"""
moving_avg.py
Author: Carl Barcenas
Contains functions related to obtaining a stock's moving average, plotting the moving average, and checking for
cross patterns via stock history.
"""

# import packages
import robin_stocks as r
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Currently using my own Robinhood account.
# Used to login to a Robinhood account.
password = input('Enter your password : ')
login = r.login('carlbarcenas95@gmail.com', password)


def get_moving_average(ticker, range):
    """
    Obtains the moving average of from stock historical data
    :param ticker: The stock to be analyzed
    :param range:
    :return:
    """
    # Access data and convert to pandas DataFrame
    # Note: pd_history and close_prices has the most recent entry at the end (index of -1)
    history = r.get_historicals(ticker, span='year', bounds='regular')
    pd_history = pd.DataFrame(history)
    close_prices = pd_history['close_price'].astype(float)
    dates = pd_history['begins_at']

    # Calculate moving average based off the range
    i = 0
    moving_average = []
    while i < len(close_prices) - range + 1:
        window = close_prices[i: i + range]
        window_avg = sum(window) / range
        moving_average.append(window_avg)
        i += 1

    dict = {'moving_average(' + str(range) + ')': moving_average,
            'date': dates[range - 1: len(dates)]}
    return pd.DataFrame(dict)


def merge_data(ticker, n_short, n_long):
    """
    Creates a singular panda DataFrame of the short and long moving averages.

    Args:
        ticker(str): Symbol of the stock to be evaluated
        n_short(int): range of the short range moving average
        n_long(int): range of the long range moving average

    Returns:
        Panda DataFrame of the short and long moving averages
    """
    # Create moving average data sets
    short = get_moving_average(ticker, n_short)
    long = get_moving_average(ticker, n_long)

    # Find difference in short and longs's indexes
    initial_index_short = short.iloc[0].name
    initial_index_long = long.iloc[0].name
    delta_initial = initial_index_long - initial_index_short

    # Update and merge the two moving averages
    short = short.iloc[delta_initial:]
    col_order = ['moving_average(' + str(n_short) + ')', 'moving_average(' + str(n_long) + ')', 'date']
    moving_averages = pd.merge(short, long).reindex(columns=col_order)

    return moving_averages


def check_cross(data):
    """
    Args:
         data(pandas.DataFrame): DataFrame of short and long moving averages

    Returns:
        1 if the intersection shows a golden cross
        0 if the intersection shows a death cross
        -1 if there is no intersection
    """
    # Set up data
    short_pts = np.array(data.iloc[:, 0])
    long_pts = np.array(data.iloc[:, 1])

    # Identify moving average intersections
    idx = np.argwhere(np.diff(np.sign(short_pts - long_pts))).flatten()

    # Identify how long ago the cross was
    if len(idx) != 0:
        days_ago = len(data) - idx[-1]

    # Check for intersection and intersection type
    if idx.size == 0:
        print("No Cross within the year.")  # NO CROSS
    else:
        if short_pts[idx[-1] - 1] < long_pts[idx[-1] - 1]:
            print("Golden Cross " + str(days_ago) + " days ago.")  # GOLDEN CROSS
        elif short_pts[idx[-1] - 1] > long_pts[idx[-1] - 1]:
            print("Death Cross " + str(days_ago) + " days ago.")  # DEATH CROSS


def plot_moving_averages(data):
    # Set up plot data
    x_set = range(len(data))
    short_pts = np.array(data.iloc[:, 0])
    long_pts = np.array(data.iloc[:, 1])

    # Plot data
    plt.plot(x_set, short_pts)
    plt.plot(x_set, long_pts)
    plt.xlabel("Time (days)")
    plt.ylabel("Moving Averages")
    plt.title("Moving Average vs. Time")
    plt.legend(["Short MA Data", "Long MA Data"])
    plt.show()


# TESTING
# Will use the stocks AAPL and FSLY for testing, as at the time of creation AAPL = no cross, FSLY = golden cross
# Test 1: Calculating Moving Average for short and long
fiddy = get_moving_average('FSLY', 50)
twohunnid = get_moving_average('FSLY', 200)
print(fiddy)
print(twohunnid)

# Test 2: Merging the two data sets to one moving_average set.
df = merge_data('AAPL', 50, 200)
print(df)

# Test 3: Check if there is a golden cross or not. Plot used for testing.
check_cross(df)
plot_moving_averages(df)
