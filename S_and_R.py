"""

@author: Maher Deeb
@ Warning: the author is not responsible for any lost of money or any type of lost because of using this program or its result.
The user is not completely responsible for all the consequences. The program and the results are only for educational purposes.

"""

import os
from utils.utils import load_data
from resistances_supports_extractor.window_method import extract_resistances_supports
from resistances_supports_extractor.power_calculator import scale_power, calculate_strength
from results_plotter.results_plotter import plot_resistances_supports


def main(filename, inputs):
    number_of_candles = inputs["number_of_candles"]
    minimum_window_size = inputs["minimum_window_size"]
    maximum_window_size = inputs["maximum_window_size"]
    tolerance = inputs["tolerance"]

    dataframe = load_data(filename)
    number_of_rows = dataframe.shape[0]

    unique_resistances_supports_list = extract_resistances_supports(number_of_rows,
                                                                    number_of_candles,
                                                                    minimum_window_size,
                                                                    maximum_window_size,
                                                                    dataframe)

    power_dict, maximum_hold_observed = calculate_strength(unique_resistances_supports_list,
                                                           number_of_candles,
                                                           number_of_rows,
                                                           dataframe,
                                                           tolerance)

    scaled_power_resistances_supports_list = scale_power(power_dict,
                                                         unique_resistances_supports_list,
                                                         maximum_hold_observed)

    plot_resistances_supports(dataframe,
                              unique_resistances_supports_list,
                              scaled_power_resistances_supports_list)

    return unique_resistances_supports_list, scaled_power_resistances_supports_list


if __name__ == '__main__':
    input_parameters = dict(number_of_candles=60,
                            minimum_window_size=5,
                            maximum_window_size=20,
                            tolerance=0.001)

    path = os.path.join("data", "EURUSD1440.csv")

    unique_resistances_supports_list, scaled_power_resistances_supports_list = main(path, input_parameters)
