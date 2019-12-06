# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 20:08:17 2017, prepared by Spyder

@author: Maher Deeb
@ Warning: the author is not responsible for any lost of money or any type of lost because of using this program or its result.
The user is not completely responsible for all the consequences.
The program and the results are only for educational purposes.

@Title:
   A window size method to extract and evaluate the strength of supports and resistances of Forex and
   stocks prices for a given period "t"
@keywords:
    window size method, supports and resistances,Forex, stocks, statistical methods, probabilistic methods

@description

The goal of this work is to extract the supports (S) and resistances (R) statistically using a method that I call it
"Window size method." After obtaining S and R, their strengths are evaluated using a statistical indicator. Support or
 resistance strength represents the possibility that the price is not able
to exceed. If the S or R is strong, the probability that the price will reverse at this point is high. Otherwise, we say S or R is weak.
for a given forex or stock signal f: f=[id::int,d::date,O::float,H::float,L::Low,C::float,V::int] where id is a unique value for each , d present the date
O is the open price, H is the highest price of the candle, L is the lowest price of the candle, the C is the close price and V is the volume. We assume that
the signal f has l data points which represnets the total number of candles.
for a given time period t::int which represents the number of candles that should be included we are going to choose windows that will be shifted through the data
starting from the latest value to the value l-t.

Inputs: f, t, ws_min,ws_max
outputs: S,R

the implementation will be done in Python using pandas

"""
# 1.Import libraries
import matplotlib

colors_all = list(matplotlib.colors.cnames.values())
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin

# ==============================================================================

# 2.read csv file (4h time frame will be used for this example)

f = pd.read_csv('EURUSD1440.csv', header=None)
# 2.1give names to the columns
f.columns = ['date', 'time', 'O', 'H', 'L', 'C', 'V']
# 2.3the amount of the data
l = len(f['H'])
# ==============================================================================
# 4. inputs
# 4.1 considered periods = number of days * 5 candles per day
t = 60 * 5
# 4.2 the minimum and the maximum size of the window that will explore the data
ws_min, ws_max = 5, 75
# 4.2 Initial values of the R and S
R = defaultdict(list)
S = defaultdict(list)
tot_R_S = []
# ==============================================================================
# 5. process:
for ws in range(ws_min, ws_max + 1):
    for t_i in range(l - t, l - ws + 2):
        top = max(f['H'][t_i + 1:t_i + ws])
        low = min(f['L'][t_i + 1:t_i + ws])
        # be sure that the values are unique
        if top not in R[ws]:
            R[ws].append(top)
            tot_R_S.append(top)
        if low not in S[ws]:
            S[ws].append(low)
            tot_R_S.append(low)
# ==============================================================================

# ==============================================================================
# 7. calculate the strength of the S or R
# 7.1 remove repeated values
s_tot_R_S = list(set(tot_R_S))
# define the power dict
p = {}
# initial value of maximum hold: we compare other R and S values based on it
max_h = 0
# define the accuracy in points: it is important to calculate when the price holds and when not
accu = 0.0005
# 7.2 apply the method
for j in range(len(s_tot_R_S)):
    vis = 0  # how many would be the R or S visited
    hol = 0  # how many the R or S visited holds
    for i in range(1, t):
        if f['L'][l - i] - accu <= s_tot_R_S[j] <= f['H'][
            l - i] + accu:  # R or S is visited if it is incide the highest and lowest price of the candle
            vis += 1
            if abs(f['H'][l - i] - s_tot_R_S[j]) < accu and max(f['C'][l - i:l - i + 2]) < s_tot_R_S[
                j]:  # R holds if the highest price stops at R and the next candle close under the R
                hol += 1
            if abs(f['L'][l - i] - s_tot_R_S[j]) < accu and min(f['C'][l - i:l - i + 2]) > s_tot_R_S[
                j]:  # S holds if the lowest price stops at S and the next candle close under the S
                hol += 1
    max_h = max(max_h, hol)
    p.update({s_tot_R_S[j]: [vis, hol, hol * 100 / vis]})
# 7.3 calculate the strength % based on the maximum number of hold (compare R and S to each other)
# low value means that R or S are not enough tested in the given period or it was not holding enought (weak)
power_S_R = []
filter_R_S = 0
for j in range(len(s_tot_R_S)):
    p[s_tot_R_S[j]][2] = p[s_tot_R_S[j]][1] * 100 / max_h
    if p[s_tot_R_S[j]][2] > filter_R_S:
        power_S_R.append(p[s_tot_R_S[j]][2])
    else:
        power_S_R.append(0)
# ==============================================================================
# 8. For visualization purposes only the R and S values close to the current price will be presented
# 8.1 current price is the close of the last candle
cur = f['C'][len(f['C']) - 1]
# 8.2 define the range of presenting the data based on the range of price movement which is the difference between the highest and lowest value of each candle
df_h_l = f['H'] - f['L']
# 8.2.1 Histogram of the price movement can be checked to understand the results.
# plt.hist(df_h_l)
# 8.3 Printing the results
fig = plt.figure()
# 8.4 plot the result
ax = fig.add_subplot(111)
ax.plot([0, 100], [cur, cur], label='current price')
ax.set_xlim(0, 100)
ax.barh(s_tot_R_S, power_S_R, align='center',
        color='green', ecolor='black', height=0.0001, label='R or S')
ax.set_ylim(cur - df_h_l.mean(), cur + df_h_l.mean())
ax.set_xlabel('Strength of R and S %')
ax.set_ylabel('Price')
ax.set_title('Current price and the closest support and resistances and their strengths')
ax.grid(True)
ax.legend()
# ==============================================================================
# 9. Apply k-mean to cluster the R and S
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
