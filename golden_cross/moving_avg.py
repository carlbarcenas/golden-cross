"""
moving_avg.py
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
print('===LOGIN TO ROBINHOOD===')
username = input('Enter your username: ')
password = input('Enter your password: ')
login = r.login(username, password)


def get_moving_average(ticker, n):
    """
    Obtains the moving average of from stock historical data
    :param ticker: The stock to be analyzed
    :param n: The day range of the moving average that is being obtained (ie 50-day moving average)
    :return: Pandas df containing the list of moving averages
    """
    # Access data and convert to pandas DataFrame
    # Note: pd_history and close_prices has the most recent entry at the end (index of -1)
    history = r.get_historicals(ticker, span='year', bounds='regular')  # gets stock historical prices
    pd_history = pd.DataFrame(history)  # transforms data obtained as a dataframe
    close_prices = pd_history['close_price'].astype(float)  # get close market prices
    dates = pd_history['begins_at']  # gets date of prices

    # Calculate moving average based off the range
    i = 0
    moving_average = []
    while i < len(close_prices) - n + 1:
        window = close_prices[i: i + n]
        window_avg = sum(window) / n
        moving_average.append(window_avg)
        i += 1

    movAvgdf = {'moving_average(' + str(n) + ')': moving_average,
                'date': dates[n - 1: len(dates)]}
    return pd.DataFrame(movAvgdf)


def merge_data(ticker, n_short, n_long):
    """
    Creates a singular panda DataFrame of the short and long moving averages
    :param ticker: Symbol of the stock to be evaluated
    :param n_short: Range of the short range moving average (in days)
    :param n_long: Range of the long range moving average (in days)
    :return: DataFrame of the short and long moving averages
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
    Checks for a golden cross within a dataframe of 2 moving average historicals
    :param data: Dataframe of the short and long moving averages
    :return: 1 if golden cross, 0 if death cross, -1 if no intersection
    """
    # Set up data
    short_pts = np.array(data.iloc[:, 0])
    long_pts = np.array(data.iloc[:, 1])

    # Identify moving average intersections
    i = 1
    idx = -1
    # Loop through the 2 arrays looking for an intersection. Idx holds index of intersection
    while i < len(short_pts):
        if short_pts[i - 1] < long_pts[i - 1] and short_pts[i] >= long_pts[i]:
            idx = i
        elif short_pts[i - 1] > long_pts[i - 1] and short_pts[i] <= long_pts[i]:
            idx = i

        i += 1

    # Identify how long ago the cross was
    if idx != -1:
        days_ago = len(data) - idx

    # Check for intersection and intersection type
    if idx == -1:
        print("No Cross within the year.")  # NO CROSS
        return -1
    else:
        if short_pts[idx - 1] < long_pts[idx - 1]:
            print("Golden Cross " + str(days_ago) + " business days ago.")  # GOLDEN CROSS
            return 1
        elif short_pts[idx - 1] > long_pts[idx - 1]:
            print("Death Cross " + str(days_ago) + " business days ago.")  # DEATH CROSS
            return 0


# This function is solely for testing purposes
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
