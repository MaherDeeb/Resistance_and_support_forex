from collections import defaultdict
import concurrent.futures
import time


def get_single_top_price_in_window(dataframe, candle_i, window_size_i):
    top = max(dataframe['high'][candle_i + 1:candle_i + window_size_i])
    return top


def get_single_low_price_in_window(dataframe, candle_i, window_size_i):
    low = min(dataframe['low'][candle_i + 1:candle_i + window_size_i])
    return low


# ==============================================================================

def define_window_sizes_list(minimum_window_size, maximum_window_size):
    window_size_list = list(range(minimum_window_size, maximum_window_size + 1))
    return window_size_list


def define_number_of_candles_list(number_of_rows, number_of_candles, window_size_i):
    candle_list = list(range(number_of_rows - number_of_candles, number_of_rows - window_size_i + 2))
    return candle_list


def extract_resistances_supports(number_of_rows: int,
                                 number_of_candles: int,
                                 minimum_window_size: int,
                                 maximum_window_size: int,
                                 dataframe):
    start_time = time.perf_counter()
    resistances_supports_list = []
    #  Initial values of the resistances and supports
    resistances = defaultdict(list)
    supports = defaultdict(list)

    for window_size_i in range(minimum_window_size, maximum_window_size + 1):
        for candle_i in range(number_of_rows - number_of_candles, number_of_rows - window_size_i + 2):
            top = get_single_top_price_in_window(dataframe, candle_i, window_size_i)
            low = get_single_low_price_in_window(dataframe, candle_i, window_size_i)
            # be sure that the values are unique
            if top not in resistances[window_size_i]:
                resistances[window_size_i].append(top)
                resistances_supports_list.append(top)
            if low not in supports[window_size_i]:
                supports[window_size_i].append(low)
                resistances_supports_list.append(low)

    unique_resistances_supports_list = list(set(resistances_supports_list))
    end_time = time.perf_counter()
    print("function without multiprocessing finished in: ", round(end_time - start_time, 2))

    return unique_resistances_supports_list
