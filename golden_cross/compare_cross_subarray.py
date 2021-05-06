"""
compare_cross_subarray.py
Essentially the main fella. Will compare
"""

import golden_cross.moving_avg as g
import golden_cross.max_subarray as ms


def cross_vs_maxsubarray(ticker):
    # Get max subarray
    arrayData = ms.get_array(ticker)
    maxSubarrayResults = ms.find_max_subarray(arrayData, 0, len(arrayData) - 1)

    # Get starting index of max subarray
    msStart = maxSubarrayResults[0]

    # Find Golden Cross index
    crossData = g.merge_data(ticker, 50, 200)
    crossResults = g.check_cross(crossData)
    if crossResults[0] == 1:
        crossIndex = crossResults[1]
    else:
        print("No golden cross, thus test not possible")
        return -1

    if abs(crossIndex - msStart) >= 10:
        print("Golden Cross aligns with Max Subarray")
        return 1
    else:
        print("Golden Cross does not align with Max Subarray")
        return 0
