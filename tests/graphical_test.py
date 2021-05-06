import golden_cross.compare_cross_subarray as ccs
import robin_stocks as r
import golden_cross.max_subarray as ms
import golden_cross.moving_avg as g
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def graph():
    # the graph data frame
    ticker = 'MGNX'
    history = r.get_historicals(ticker, span='year', bounds='regular')  # gets stock historical prices
    pd_history = pd.DataFrame(history)  # transforms data obtained as a dataframe
    close_prices = pd_history['close_price'].astype(float)  # get close market prices
    resized_close_prices = np.array(close_prices[len(close_prices) - 54: len(close_prices) - 1])
    derivative_close_prices = ms.get_array(ticker)
    # ADDED BY CARL
    df_cross = g.merge_data('MGNX', 50, 200)
    # x_set = range(len(df))
    short_pts = np.array(df_cross.iloc[:, 0])
    long_pts = np.array(df_cross.iloc[:, 1])
    # plot df
    df = pd.DataFrame({'x_values': range(len(resized_close_prices)), 'Value ($)': resized_close_prices,
                       'Change in Value': derivative_close_prices, "Short MA": short_pts, "Long MA": long_pts})
    plt.plot('x_values', 'Value ($)', data=df, marker='o', markerfacecolor='red', markersize=12, color='skyblue',
             linewidth=4)
    plt.plot('x_values', 'Change in Value', data=df, marker='o', color='blue', linewidth=2)
    plt.plot('x_values', 'Short MA', data=df, color='blue', linewidth=3)
    plt.plot('x_values', 'Long MA', data=df, color='orange', linewidth=3)
    # span the plot over the maximum subarray
    max_subarray = ms.find_max_subarray(derivative_close_prices, 0, len(resized_close_prices) - 1)
    max_subarray_left = max_subarray[0]  # left side
    max_subarray_right = max_subarray[1]  # right side
    # plot the maximum subarray span
    plt.axvspan(max_subarray_left, max_subarray_right, color='green', alpha=0.5)
    # plot a line at where the golden cross occurs
    # finish graph settings
    x_label = "Date"
    plt.xlabel(x_label)
    plt.ylabel('Value ($)')
    plt.title('Value and Change in Value With Maximum Subarray Overlay')
    # plt.plot(x_set, short_pts)
    # plt.plot(x_set, long_pts)
    # plt.legend(["Value ($)", "Change in Value", "Short MA Data", "Long MA Data"])
    # show legend
    plt.legend()
    # show graph
    plt.show()


graph()