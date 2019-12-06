"""

@author: Maher Deeb
@ Warning: the author is not responsible for any lost of money or any type of lost because of using this program or its result.
The user is not completely responsible for all the consequences. The program and the results are only for educational purposes.

"""

# 1.Import libraries
import matplotlib

colors_all = list(matplotlib.colors.cnames.values())
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin

from utils.utils import load_data


def main(filename):
    dataframe = load_data(filename)


if __name__ == '__main__':
    # Inputs
    # considered periods = number of days * 5 candles per day if the frequency is 4 hours
    # number_of_candles = 60 * 5
    # the minimum and the maximum size of the window that will explore the data
    # minimum_window_size, maximum_window_size = 5, 75
    #  Initial values of the resistances and supports
    resistances = defaultdict(list)
    supports = defaultdict(list)

    # define the power dict
    # p = {}
    # initial value of maximum hold: we compare other resistances and supports values based on it
    # max_h = 0
    # define the accuracy in points: it is important to calculate when the price holds and when not
    # accu = 0.0005

    main()


def get_single_top_price_in_window(dataframe, candle_i, window_size_i):
    top = max(dataframe['high'][candle_i + 1:candle_i + window_size_i])
    return top


def get_single_low_price_in_window(dataframe, candle_i, window_size_i):
    low = min(dataframe['low'][candle_i + 1:candle_i + window_size_i])
    return low


# ==============================================================================
# 5. process:
def extract_resistances_supports(number_of_rows: int,
                                 number_of_candles: int,
                                 minimum_window_size: int,
                                 maximum_window_size: int,
                                 dataframe):
    resistances_supports_list = []

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
    return resistances_supports_list


# ==============================================================================

# ==============================================================================
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


def calculate_strength(resistances_supports_list,
                       number_of_candles,
                       number_of_rows,
                       dataframe,
                       tolerance):
    unique_resistances_supports_list = list(set(resistances_supports_list))

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
    power_resistances_supports_list = []
    power_threshold = 0
    for price_i in unique_resistances_supports_list:
        power_dict[price_i][2] = power_dict[price_i][1] * 100 / maximum_hold_observed
        if power_dict[price_i][2] > power_threshold:
            power_resistances_supports_list.append(power_dict[price_i][2])
        else:
            power_resistances_supports_list.append(0)
    return power_dict


# ==============================================================================
# 8. For visualization purposes only the resistances and supports values close to the current price will be presented
# 8.1 current price is the close of the last candle
cur = dataframe["close"][len(dataframe["close"]) - 1]
# 8.2 define the range of presenting the data based on the range of price movement which is the difference between the highest and lowest value of each candle
df_h_l = dataframe["high"] - dataframe["low"]
# 8.2.1 Histogram of the price movement can be checked to understand the results.
# plt.hist(df_h_l)
# 8.3 Printing the results
fig = plt.figure()
# 8.4 plot the result
ax = fig.add_subplot(111)
ax.plot([0, 100], [cur, cur], label='current price')
ax.set_xlim(0, 100)
ax.barh(s_tot_R_S, power_S_R, align='center',
        color='green', ecolor='black', height=0.0001, label='resistances or supports')
ax.set_ylim(cur - df_h_l.mean(), cur + df_h_l.mean())
ax.set_xlabel('Strength of resistances and supports %')
ax.set_ylabel('Price')
ax.set_title('Current price and the closest support and resistances and their strengths')
ax.grid(True)
ax.legend()
# ==============================================================================
# 9. Apply k-mean to cluster the resistances and supports
# 9.1 choose K
K = 100
init_arr = []
for i in range(len(s_tot_R_S)):
    init_arr.append([s_tot_R_S[i], power_S_R[i]])
    # init_arr.append([power_S_R[i],s_tot_R_S[i]])

X = np.array(init_arr)
kmeans = KMeans(n_clusters=K, random_state=0, n_init=500, max_iter=1000).fit(X)

resu = kmeans.cluster_centers_

colors = colors_all[0:K]

k_means_cluster_centers = resu  # np.sort(resu, axis=0)
k_means_labels = pairwise_distances_argmin(X, k_means_cluster_centers)
print(resu[:, 0])
# ==============================================================================
fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.plot(resu[:, 0], resu[:, 1], '*')
# ==============================================================================
fig2 = plt.figure()

ax = fig2.add_subplot(1, 1, 1)
for k, col in zip(range(K), colors):
    my_members = k_means_labels == k
    cluster_center = k_means_cluster_centers[k]
    ax.plot(X[my_members, 0], X[my_members, 1], '*',
            markerfacecolor=col, markersize=2)
    ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=5)
ax.set_title('KMeans')
ax.set_xticks(())
ax.set_yticks(())
# plt.text(-3.5, 1.8,  'train time: %.2fs\ninertia: %f' % (
#    t_batch, k_means.inertia_))
