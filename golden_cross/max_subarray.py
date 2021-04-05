"""
moving_avg.py
Contains functions used to find the Maximum Subarray of a stock
"""

import robin_stocks as r
import pandas as pd
import numpy as np
import math

# IT SHOULD BE IMPORTANT TO NOTE THAT DUE TO THE LIMITATIONS
# OF GATHERING STOCK HISTORICAL DATA, LOW IS ALWAYS 0 AND
# HIGH IS ALWAYS 52

def findMaxCrossingSubarray(A, low, mid, high):
    leftSum = -math.inf
