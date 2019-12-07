import os
from S_and_R import main
from utils.utils import load_data

if __name__ == '__main__':
    input_parameters = dict(number_of_candles=60,
                            minimum_window_size=5,
                            maximum_window_size=20,
                            tolerance=0.001)

    path = os.path.join("data", "EURUSD1440.csv")
    dataframe = load_data(path)
    unique_resistances_supports_list, scaled_power_resistances_supports_list = main(dataframe, input_parameters)
