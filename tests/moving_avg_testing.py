import golden_cross.moving_avg as g
import numpy as np
import time

# TODO: Switch case testing

def test1():
    # Will use the stocks AAPL and FSLY for testing, as at the time of creation AAPL = no cross, FSLY = golden cross
    # Test 1: Calculating Moving Average for short and long
    fiddy = g.get_moving_average('FSLY', 50)
    twohunnid = g.get_moving_average('FSLY', 200)
    print(len(fiddy))
    print(len(twohunnid))
    print(fiddy)
    print(twohunnid)

def test2():
    # Test 2: Merging the two data sets to one moving_average set.
    df = g.merge_data('AAPL', 50, 200)
    print(df)
    # Test 3: Check if there is a golden cross or not. Plot used for testing.
    g.check_cross(df)
    g.plot_moving_averages(df)

def test3(): # Runtime
    df = g.merge_data('MGNX', 50, 200)

    # Change size of dataframe for testing.
    df = df.drop([50])

    start = time.perf_counter()
    g.check_cross(df)
    stop = time.perf_counter()

    print("Runtime is " + str(stop - start))

# Run test here:
test2()
