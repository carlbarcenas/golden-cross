import golden_cross.max_subarray as ms


def test1():
    # See if get_array gets the daily stock price change
    # Uncomment the print statement in get_array() to compare stock prices.
    testArray = ms.get_array("AAPL")
    print(testArray)
    print(len(testArray))

def test2():
    # Test get_max_subarray()
    A = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7] # From textbook p.70
    print("Expected: [7, 10, 43]")
    print("Actual: ", ms.find_max_subarray(A, 0, len(A)-1))

def test3():
    # Test actual maximum subarray run
    A = ms.get_array('MGNX')
    print(ms.find_max_subarray(A, 0, len(A)-1))


# TEST HERE: choose your tests
test3()
