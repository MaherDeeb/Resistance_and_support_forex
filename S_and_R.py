"""

@author: Maher Deeb
@ Warning: the author is not responsible for any lost of money or any type of lost because of using this program or its result.
The user is not completely responsible for all the consequences. The program and the results are only for educational purposes.

"""

from utils.utils import load_data
from resistances_supports_extractor.window_method import extract_resistances_supports
from resistances_supports_extractor.power_calculator import scale_power, calculate_strength
from results_plotter.results_plotter import plot_resistances_supports


def main(filename, inputs):
    number_of_rows = inputs["number_of_rows"]
    number_of_candles = inputs["number_of_candles"]
    minimum_window_size = inputs["minimum_window_size"]
    maximum_window_size = inputs["maximum_window_size"]
    tolerance = inputs["tolerance"]

    dataframe = load_data(filename)

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

    return unique_resistances_supports_list, scaled_power_resistances_supports_list


if __name__ == '__main__':
    # Inputs
    # considered periods = number of days * 5 candles per day if the frequency is 4 hours
    # number_of_candles = 60 * 5
    # the minimum and the maximum size of the window that will explore the data
    # minimum_window_size, maximum_window_size = 5, 75

    # define the power dict
    # p = {}
    # initial value of maximum hold: we compare other resistances and supports values based on it
    # max_h = 0
    # define the accuracy in points: it is important to calculate when the price holds and when not
    # accu = 0.0005

    main()
