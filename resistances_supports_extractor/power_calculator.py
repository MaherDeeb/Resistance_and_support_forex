# 7. calculate the strength of the supports or resistances
# 7.1 remove repeated values


def lowest_highest_candle_price(dataframe, number_of_rows, candle_i, tolerance):
    lowest_candle_price = dataframe["low"][number_of_rows - candle_i] - tolerance
    highest_candle_price = dataframe["high"][number_of_rows - candle_i] + tolerance
    return lowest_candle_price, highest_candle_price


def resistances_hold(hold_price, price_i, dataframe, number_of_rows, candle_i, tolerance):
    # resistances holds if the highest price stops at those
    # resistances and the next candle close under those resistances
    if abs(dataframe["high"][number_of_rows - candle_i] - price_i) < tolerance and max(
            dataframe["close"][number_of_rows - candle_i:number_of_rows - candle_i + 2]) < \
            price_i:
        hold_price += 1
    return hold_price


def supports_hold(hold_price, price_i, dataframe, number_of_rows, candle_i, tolerance):
    # supports holds if the lowest price stops at supports and the next candle close under the supports
    if abs(dataframe["low"][number_of_rows - candle_i] - price_i) < tolerance and min(
            dataframe["close"][number_of_rows - candle_i:number_of_rows - candle_i + 2]) > price_i:
        hold_price += 1
    return hold_price


def calculate_strength(unique_resistances_supports_list,
                       number_of_candles,
                       number_of_rows,
                       dataframe,
                       tolerance):
    maximum_hold_observed = 0
    power_dict = {}

    for price_i in unique_resistances_supports_list:

        # how many times would be the resistances or supports visited independent of they are exceeded or price reversed
        visited_price = 0
        # how many times the resistances or supports that are visited visited hold
        # i.e. price reverse after reaching those prices
        hold_price = 0  # how many the resistances or supports visited holds

        for candle_i in range(1, number_of_candles):
            # resistances or supports is visited if it is inside the highest and lowest price of the candle
            lowest_candle_price, highest_candle_price = lowest_highest_candle_price(dataframe,
                                                                                    number_of_rows,
                                                                                    candle_i,
                                                                                    tolerance)
            if lowest_candle_price <= price_i <= highest_candle_price:
                visited_price += 1
                # resistances holds if the highest price stops at those
                # resistances and the next candle close under those resistances

                hold_price = resistances_hold(hold_price, price_i, dataframe, number_of_rows, candle_i, tolerance)
                hold_price = supports_hold(hold_price, price_i, dataframe, number_of_rows, candle_i, tolerance)

        maximum_hold_observed = max(maximum_hold_observed, hold_price)

        power_dict.update({price_i: [visited_price, hold_price, hold_price * 100 / visited_price]})

    return power_dict, maximum_hold_observed

    # 7.3 calculate the strength % based on the maximum number of hold (compare resistances and supports to each other)
    # low value means that resistances or supports are not enough tested in the given period or it was not holding enought (weak)


def scale_power(power_dict, unique_resistances_supports_list, maximum_hold_observed):
    scaled_power_resistances_supports_list = []
    power_threshold = 0
    for price_i in unique_resistances_supports_list:
        power_dict[price_i][2] = power_dict[price_i][1] * 100 / maximum_hold_observed
        if power_dict[price_i][2] > power_threshold:
            scaled_power_resistances_supports_list.append(power_dict[price_i][2])
        else:
            scaled_power_resistances_supports_list.append(0)
    return scaled_power_resistances_supports_list
