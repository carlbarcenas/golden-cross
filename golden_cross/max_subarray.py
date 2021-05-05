"""
moving_avg.py
Contains functions used to find the Maximum Subarray of a stock
"""

import robin_stocks as r
import pandas as pd
import numpy as np
import math

# Currently using my own Robinhood account.
# Used to login to a Robinhood account.
print('===LOGIN TO ROBINHOOD===')
username = input('Enter your username: ')
password = input('Enter your password: ')
login = r.login(username, password)

"""
IT SHOULD BE IMPORTANT TO NOTE THAT DUE TO THE LIMITATIONS
OF GATHERING STOCK HISTORICAL DATA, LOW IS ALWAYS 0 AND 
HIGH IS ALWAYS 52.
To put it briefly, we are only given a year's worth of data for
stock prices, and thus that limits our 200 day MA to 53 entries in
it's array.
Thus, for the sake of the project we can only find the max subarray within
the previous 53 business days.
"""


def get_array(ticker):
    # See above statement, find the past 54 entries and calculate change in price
    history = r.get_historicals(ticker, span='year', bounds='regular')  # gets stock historical prices
    pd_history = pd.DataFrame(history)  # transforms data obtained as a dataframe
    close_prices = pd_history['close_price'].astype(float)  # get close market prices
    resized_close_prices = np.array(close_prices[len(close_prices) - 54: len(close_prices)])

    i = 1
    derivative_array = [0] * 53
    while i < len(resized_close_prices):
        derivative_array[i - 1] = resized_close_prices[i] - resized_close_prices[i - 1]
        i += 1

    return derivative_array


def find_max_crossing_subarray(A, low, mid, high):
    leftSum = -math.inf
    sum = 0

    i = mid
    while mid >= low:  # Im not sure if its >= or just >
        sum = sum + A[i]
        if sum > leftSum:
            leftSum = sum
            maxLeft = i
        i -= 1

    rightSum = -math.inf
    sum = 0

    j = mid + 1
    while j <= high:
        sum = sum + A[j]
        if sum > rightSum:
            rightSum = sum
            maxRight = j
        j -= 1

    return (maxLeft, maxRight, leftSum + rightSum)


def find_max_subarray(A, low, high):
    if high == low:  # Base case
        return (low, high, A[low])
    else:
        mid = math.floor((low + high) / 2)
        (leftLow, leftHigh, leftSum) = find_max_subarray(A, low, mid)
        (rightLow, rightHigh, rightSum) = find_max_subarray(A, mid + 1, high)
        (crossLow, crossHigh, crossSum) = find_max_crossing_subarray(A, low, mid, high)
        if leftSum >= rightSum and leftSum >= crossSum:
            return (leftLow, leftHigh, leftSum)
        elif rightSum >= leftSum and rightSum >= crossSum:
            return (rightLow, rightHigh, rightSum)
        else:
            return (crossLow, crossHigh, crossSum)
