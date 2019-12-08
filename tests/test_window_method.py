import unittest
from resistances_supports_extractor.window_method import get_single_top_price_in_window, \
    get_single_low_price_in_window, define_window_sizes_list, define_number_of_candles_list
import pandas as pd
import numpy as np

dataframe = pd.DataFrame(index=range(10), columns=["date", "hour", "open", "high", "close", "volume"])

dataframe["date"] = [f"2019-05-0{x}" if x < 10 else f"2019-05-{x}" for x in range(1, 11)]
dataframe["hour"] = ["00:00" for _ in range(1, 11)]
dataframe["open"] = [2, 3, 4, 5, 6, 7, 6, 5, 4, 3]
dataframe["high"] = [5, 6, 7, 8, 9, 9, 8, 9, 7, 6]
dataframe["low"] = [1, 1, 2, 3, 1, 3, 3, 2, 2, 1]
dataframe["close"] = [3, 2, 3, 5, 4, 3, 7, 7, 7, 6]
dataframe["volume"] = np.random.randint(100, size=10)


# window_size = 3
# candle_i = 0
# print(dataframe['high'][candle_i + 1:candle_i + window_size])


class MyTestCase(unittest.TestCase):
    def test_top_price(self):
        window_size = 3
        candle_i = 0
        highest_price = get_single_top_price_in_window(dataframe, candle_i, window_size)
        self.assertEqual(highest_price, 7)

    def test_low_price(self):
        window_size = 3
        candle_i = 0
        lowest_price = get_single_low_price_in_window(dataframe, candle_i, window_size)
        self.assertEqual(lowest_price, 1)

    def test_define_window_sizes_list(self):
        minimum_window_size = 3
        maximum_window_size = 7
        window_list = define_window_sizes_list(minimum_window_size, maximum_window_size)
        self.assertEqual(window_list, [3, 4, 5, 6, 7])

    def test_define_number_of_candles_list(self):
        number_of_rows = 10 # dataframe.shape[0]
        number_of_candles = 5
        window_size_i = 4
        candle_list = define_number_of_candles_list(number_of_rows, number_of_candles, window_size_i)
        self.assertEqual(candle_list, [5, 6, 7])


if __name__ == '__main__':
    unittest.main()
