import matplotlib.pyplot as plt


# ==============================================================================
# 8. For visualization purposes only the resistances and supports values close to the current price will be presented
# 8.1 current price is the close of the last candle

def current_price_extractor(dataframe):
    current_price = dataframe["close"][len(dataframe["close"]) - 1]
    return current_price


# 8.2 define the range of presenting the data based on the range of price movement which is the difference between
# the highest and lowest value of each candle
def price_movement_range(dataframe):
    price_range = dataframe["high"] - dataframe["low"]
    return price_range


# 8.2.1 Histogram of the price movement can be checked to understand the results.
# plt.hist(df_h_l)
# 8.3 Printing the results
def plot_resistances_supports(dataframe,
                              unique_resistances_supports_list,
                              scaled_power_resistances_supports_list):
    current_price = current_price_extractor(dataframe)
    price_range = price_movement_range(dataframe)
    fig = plt.figure()
    # 8.4 plot the result
    ax = fig.add_subplot(111)
    ax.plot([0, 100], [current_price, current_price], label='current price')
    ax.set_xlim(0, 100)
    ax.barh(unique_resistances_supports_list, scaled_power_resistances_supports_list, align='center',
            color='green', ecolor='black', height=0.0001, label='resistances or supports')
    ax.set_ylim(current_price - price_range.mean(), current_price + price_range.mean())
    ax.set_xlabel('Strength of resistances and supports %')
    ax.set_ylabel('Price')
    ax.set_title('Current price and the closest support and resistances and their strengths')
    ax.grid(True)
    ax.legend()
