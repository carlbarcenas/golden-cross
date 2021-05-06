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
    tempArray = [0] * 3 # Holds low, mid, high

    for i in range(mid, low-1, -1):  # Im not sure if its >= or just >
        sum = sum + A[i]
        if sum > leftSum:
            leftSum = sum
            maxLeft = i


    rightSum = -math.inf
    sum = 0
    for i in range(mid + 1, high + 1):
        sum = sum + A[i]
        if sum > rightSum:
            rightSum = sum
            maxRight = i

    tempArray[0] = maxLeft
    tempArray[1] = maxRight
    tempArray[2] = leftSum + rightSum

    return tempArray


def find_max_subarray(array, low, high):
    tempArrayBase = [low, high, array[low]]
    tempArrayLeft = [0] * 3  #Holds leftLow, leftHigh, leftSum in order of index
    tempArrayRight = [0] * 3  #Holds rightLow, rightHigh, rightSum in order of index
    tempArrayCross = [0] * 3  #Holds crossLow, crossHigh, crossSum in order of index

    if high == low:  # Base case
        return tempArrayBase
    else:
        mid = (low + high) // 2
        tempArrayLeft = find_max_subarray(array, low, mid)
        tempArrayRight = find_max_subarray(array, mid + 1, high)
        tempArrayCross = find_max_crossing_subarray(array, low, mid, high)
        if tempArrayLeft[2] >= tempArrayRight[2] and tempArrayLeft[2] >= tempArrayCross[2]:
            return tempArrayLeft
        elif tempArrayRight[2] >= tempArrayLeft[2] and tempArrayRight[2] >= tempArrayCross[2]:
            return tempArrayRight
        else:
            return tempArrayCross
